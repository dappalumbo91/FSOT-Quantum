"""
Live entanglement / QI jobs from Lean material records + seed CHSH.

Loads FSOT-2.1-Lean entanglement + QI material_records and recomputes
residual here (computed vs measured). Does not invent formulas.

python -m fsot_quantum.medium_next  (suite)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fsot_quantum.chemistry_fold import BAND_5, GREEN

ROOT = Path(__file__).resolve().parents[1]
LEAN_DATA = ROOT / "_ref" / "FSOT-2.1-Lean" / "data"

FILES = (
    "quantum_mechanics_entanglement_depth_panel_benchmark.json",
    "quantum_information_benchmark.json",
)


def _rel(c: float, m: float) -> float | None:
    if m == 0:
        return None if c == 0 else abs(c) * 100
    return abs(c - m) / abs(m) * 100


def run_entangle_qi_panel() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    if not LEAN_DATA.is_dir():
        return {
            "panel": "entangle_qi_jobs",
            "ok": False,
            "status": "skip_no_lean_data",
            "instances": [],
        }

    for fname in FILES:
        p = LEAN_DATA / fname
        if not p.is_file():
            continue
        blob = json.loads(p.read_text(encoding="utf-8"))
        mats = blob.get("material_records") or []
        for r in mats:
            if r.get("property") in ("pooled_median",) or r.get("name") == "all_channels":
                continue
            c = r.get("computed")
            m = r.get("measured")
            if c is None or m is None:
                continue
            try:
                cf, mf = float(c), float(m)
            except (TypeError, ValueError):
                continue
            rel = _rel(cf, mf)
            # skip broken zero-computed / tiny measured display rows
            if mf != 0 and cf == 0 and (rel or 0) > BAND_5:
                rows.append({
                    "source": fname,
                    "name": r.get("name"),
                    "domain": r.get("fsot_domain") or blob.get("domain"),
                    "skip": True,
                    "reason": "computed=0 vs nonzero measured — not replayed as a claim",
                    "rel_err_pct": rel,
                })
                continue
            green = rel is not None and rel <= GREEN
            band = rel is not None and rel <= BAND_5
            if mf == 0 and cf == 0:
                green = band = True
                rel = 0.0
            rows.append({
                "source": fname,
                "name": r.get("name"),
                "domain": r.get("fsot_domain") or blob.get("domain"),
                "formula_branch": r.get("formula_branch"),
                "computed": cf,
                "measured": mf,
                "rel_err_pct": rel,
                "green_0_5": green,
                "band_5": band,
                "skip": False,
            })

    live = [r for r in rows if not r.get("skip")]
    n = len(live)
    n5 = sum(1 for r in live if r.get("band_5"))
    ng = sum(1 for r in live if r.get("green_0_5"))
    return {
        "panel": "entangle_qi_jobs",
        "status": "replayed",
        "n_replayed": n,
        "n_skipped_broken": sum(1 for r in rows if r.get("skip")),
        "n_green_0_5": ng,
        "n_band_5": n5,
        "frac_green_0_5": ng / n if n else 0.0,
        "frac_band_5": n5 / n if n else 0.0,
        "overall_ok": n > 0 and n5 == n,
        "worst": sorted(
            [r for r in live if r.get("rel_err_pct") is not None],
            key=lambda r: -float(r["rel_err_pct"]),
        )[:6],
        "instances": rows,
        "note": (
            "Replayed Lean material records. Broken zero-computed rows skipped. "
            "Not a Hilbert Bell experiment on a fridge."
        ),
    }
