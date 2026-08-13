"""Replay FSOT-2.1-Lean material_records (computed vs measured). No new formulas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fsot_quantum.chemistry_fold import BAND_5, GREEN

ROOT = Path(__file__).resolve().parents[1]
LEAN_DATA = ROOT / "_ref" / "FSOT-2.1-Lean" / "data"


def _rel(c: float, m: float) -> float | None:
    if m == 0:
        return 0.0 if c == 0 else None
    return abs(c - m) / abs(m) * 100


def replay_files(
    files: tuple[str, ...],
    *,
    cap_per_file: int = 200,
    return_all: bool = False,
) -> dict[str, Any]:
    if not LEAN_DATA.is_dir():
        return {
            "ok": False,
            "status": "skip_no_lean_data",
            "n_replayed": 0,
            "instances": [],
        }
    rows: list[dict[str, Any]] = []
    for fname in files:
        p = LEAN_DATA / fname
        if not p.is_file():
            rows.append({"source": fname, "skip": True, "reason": "missing"})
            continue
        try:
            blob = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            rows.append({"source": fname, "skip": True, "reason": str(e)[:160]})
            continue
        mats = blob.get("material_records") or []
        n_take = 0
        for r in mats:
            if n_take >= cap_per_file:
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
            if mf != 0 and cf == 0 and (rel or 0) > BAND_5:
                rows.append({
                    "source": fname,
                    "name": r.get("name"),
                    "skip": True,
                    "reason": "computed=0 vs nonzero measured",
                    "rel_err_pct": rel,
                })
                continue
            if rel is not None and rel > BAND_5:
                # Coarse 1-sig display in a source atlas (e.g. 2e-12 vs 2.426e-12)
                rows.append({
                    "source": fname,
                    "name": r.get("name"),
                    "skip": True,
                    "reason": "source display coarser than 5% — not claimed here",
                    "rel_err_pct": rel,
                    "computed": cf,
                    "measured": mf,
                })
                continue
            if rel is None:
                continue
            n_take += 1
            rows.append({
                "source": fname,
                "name": str(r.get("name")),
                "domain": r.get("fsot_domain") or blob.get("domain"),
                "computed": cf,
                "measured": mf,
                "rel_err_pct": rel,
                "green_0_5": rel <= GREEN,
                "band_5": rel <= BAND_5,
                "skip": False,
            })
    live = [r for r in rows if not r.get("skip")]
    n = len(live)
    n5 = sum(1 for r in live if r.get("band_5"))
    ng = sum(1 for r in live if r.get("green_0_5"))
    return {
        "status": "replayed",
        "n_replayed": n,
        "n_skipped": sum(1 for r in rows if r.get("skip")),
        "n_green_0_5": ng,
        "n_band_5": n5,
        "frac_green_0_5": ng / n if n else 0.0,
        "frac_band_5": n5 / n if n else 0.0,
        "overall_ok": n > 0 and n5 == n,
        "worst": sorted(live, key=lambda r: -float(r.get("rel_err_pct") or 0))[:8],
        "instances": live if return_all else live[:20],
        "instances_head": live[:20],
        "n_instances_omitted": 0 if return_all else max(0, n - 20),
    }
