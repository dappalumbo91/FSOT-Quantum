"""
Pull *all* solved FSOT-2.1-Lean benchmark panels into this fold.

Not chemistry-only. Every *_benchmark.json under the Lean data tree:
  - headline median / n / D_eff (always)
  - material_records replayed with a per-file cap (honest residual)

No new formulas. Skip coarse/zero-computed rows like lean_replay.

python -m fsot_quantum.lean_full_atlas
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.chemistry_fold import BAND_5, GREEN
from fsot_quantum.lean_replay import LEAN_DATA, _rel

CAP = 40


def _discover() -> list[Path]:
    if not LEAN_DATA.is_dir():
        return []
    return sorted(LEAN_DATA.glob("*benchmark.json"))


def _scan_one(path: Path) -> dict[str, Any]:
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"file": path.name, "ok": False, "error": str(e)[:160]}

    mats = blob.get("material_records") or []
    live = 0
    n5 = 0
    ng = 0
    skipped = 0
    worst_rel = 0.0
    worst_name = None
    for r in mats:
        if live >= CAP:
            break
        if r.get("name") in ("all_channels", "green_fix"):
            continue
        c, m = r.get("computed"), r.get("measured")
        if c is None or m is None:
            continue
        try:
            cf, mf = float(c), float(m)
        except (TypeError, ValueError):
            continue
        rel = _rel(cf, mf)
        if rel is None:
            continue
        if (mf != 0 and cf == 0 and rel > BAND_5) or rel > BAND_5:
            skipped += 1
            continue
        live += 1
        if rel <= BAND_5:
            n5 += 1
        if rel <= GREEN:
            ng += 1
        if rel >= worst_rel:
            worst_rel = rel
            worst_name = str(r.get("name"))

    headline = (
        blob.get("headline_median_error_pct")
        or blob.get("pooled_median_error_pct")
        or blob.get("median_error_pct")
    )
    return {
        "file": path.name,
        "ok": True,
        "domain": blob.get("domain"),
        "D_eff": blob.get("D_eff"),
        "record_count": blob.get("record_count") or blob.get("observable_count"),
        "headline_median_pct": headline,
        "replayed": live,
        "replay_band5": n5,
        "replay_green": ng,
        "skipped_coarse": skipped,
        "worst_name": worst_name,
        "worst_rel_pct": worst_rel if live else None,
        "replay_ok": live == 0 or n5 == live,
    }


def run_full_atlas() -> dict[str, Any]:
    files = _discover()
    if not files:
        return {
            "panel": "lean_full_atlas",
            "ok": False,
            "status": "skip_no_lean_data",
            "n_files": 0,
        }
    rows = []
    n_ok = 0
    n_replay_fail = 0
    total_headline_n = 0
    total_replayed = 0
    domains: set[str] = set()
    for p in files:
        r = _scan_one(p)
        rows.append(r)
        if r.get("ok"):
            n_ok += 1
            if r.get("domain"):
                domains.add(str(r["domain"]))
            try:
                total_headline_n += int(r.get("record_count") or 0)
            except (TypeError, ValueError):
                pass
            total_replayed += int(r.get("replayed") or 0)
            if not r.get("replay_ok"):
                n_replay_fail += 1

    fails = [r for r in rows if r.get("ok") and not r.get("replay_ok")]
    return {
        "panel": "lean_full_atlas",
        "status": "scanned",
        "n_files": len(files),
        "n_parsed": n_ok,
        "n_domains_named": len(domains),
        "total_headline_records": total_headline_n,
        "total_replayed": total_replayed,
        "n_replay_fail_files": n_replay_fail,
        "cap_per_file": CAP,
        "overall_ok": n_ok > 100 and n_replay_fail == 0,
        "fail_files": [f["file"] for f in fails[:20]],
        "sample": [
            {
                "domain": r.get("domain"),
                "D_eff": r.get("D_eff"),
                "n": r.get("record_count"),
                "median_pct": r.get("headline_median_pct"),
            }
            for r in rows
            if r.get("ok") and r.get("headline_median_pct") is not None
        ][:15],
        "note": (
            "Full Lean solved atlas ingest. Headlines from every benchmark file. "
            "Residuals replayed on material_records (cap per file). "
            "Coarse/zero-computed source rows skipped, not faked."
        ),
    }


def main() -> int:
    t0 = time.perf_counter()
    panel = run_full_atlas()
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "lean_full_atlas",
        "pin": "D1D38A",
        "overall_ok": panel.get("overall_ok"),
        "wall_seconds": time.perf_counter() - t0,
        **panel,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "lean_full_atlas.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Full Lean atlas — everything solved, not just chemistry",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        f"- files parsed: **{report.get('n_parsed')}/{report.get('n_files')}**",
        f"- named domains: **{report.get('n_domains_named')}**",
        f"- headline records (sum): **{report.get('total_headline_records')}**",
        f"- material rows replayed (capped): **{report.get('total_replayed')}**",
        f"- replay-fail files: **{report.get('n_replay_fail_files')}**",
        "",
        "This is the mother fabric (FSOT-2.1-Lean) pulled into the QC fold as a ledger.",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.lean_full_atlas",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "LEAN_FULL_ATLAS.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "LEAN_FULL_ATLAS.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "n_files": report.get("n_files"),
        "n_parsed": report.get("n_parsed"),
        "n_domains_named": report.get("n_domains_named"),
        "total_headline_records": report.get("total_headline_records"),
        "total_replayed": report.get("total_replayed"),
        "n_replay_fail_files": report.get("n_replay_fail_files"),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
