"""
Tighten chemistry residual reporting to 0.5% green band (atlas style).

Uses vendor seed formulas; reports per-observable pass at 0.5% and 5%.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GREEN = 0.5
BAND_5 = 5.0


def run_chemistry_strict_panel() -> dict[str, Any]:
    from vendor import fsot_compute as f

    waves = [
        "chemistry_bond_lengths",
        "chemistry_bond_energies",
        "chemistry_ionization",
        "chemistry_electronegativity",
        "chemistry_molecular",
        "chemistry_radii",
    ]
    all_rows = []
    for w in waves:
        fn = getattr(f, w)
        for r in fn():
            if r.measured is None or float(r.measured) == 0:
                continue
            rel = abs(float(r.computed - r.measured) / float(r.measured)) * 100
            all_rows.append({
                "wave": w,
                "name": r.name,
                "computed": float(r.computed),
                "measured": float(r.measured),
                "rel_err_pct": rel,
                "green_0_5": rel <= GREEN,
                "band_5": rel <= BAND_5,
            })

    n = len(all_rows)
    n_green = sum(1 for r in all_rows if r["green_0_5"])
    n_5 = sum(1 for r in all_rows if r["band_5"])
    errs = sorted(r["rel_err_pct"] for r in all_rows)
    median = errs[len(errs) // 2] if errs else None

    # Wave-level: ok if median within 5% (publishable chemistry panel);
    # green_fraction reported separately for 0.5% aspiration.
    report = {
        "panel": "chemistry_strict",
        "green_pct": GREEN,
        "band_5_pct": BAND_5,
        "n_observables": n,
        "n_green_0_5": n_green,
        "n_band_5": n_5,
        "frac_green_0_5": n_green / n if n else 0.0,
        "frac_band_5": n_5 / n if n else 0.0,
        "median_rel_err_pct": median,
        "overall_ok": median is not None and median <= BAND_5 and n_5 == n,
        "aspiration_0_5_ok": n_green == n,
        "worst": sorted(all_rows, key=lambda r: -r["rel_err_pct"])[:8],
        "best": sorted(all_rows, key=lambda r: r["rel_err_pct"])[:5],
        "note": "0.5% is atlas green aspiration; panel gate is all within 5% + median<=5%",
    }
    out = ROOT / "results" / "chemistry_strict.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
