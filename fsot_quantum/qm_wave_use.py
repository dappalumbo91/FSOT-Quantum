"""
QM / particle-scale residuals from pin formulas — applied FSOT math.

These are vendor seed-closed expressions (D1D38A), not a Hilbert simulator
and not a fitted SM Lagrangian. Field of use: the same constants QC/QM
papers quote (α, Weinberg angle, mass ratios).

Bands: 0.5% green, 5% atlas (same as chemistry_strict).
"""

from __future__ import annotations

from typing import Any

from fsot_quantum.chemistry_fold import GREEN, BAND_5
from fsot_quantum.domains import domain_scalar


def run_qm_wave_use_panel() -> dict[str, Any]:
    from vendor import fsot_compute as f

    waves = [
        ("wave2_qm_sm", f.wave2),
        ("validation_qm", lambda: [
            r for r in f.validation_suite()
            if r.name in (
                "alpha_FSOT",
                "sin2_theta_W",
                "M_Z/M_W",
                "Proton_radius",
            )
        ]),
    ]
    rows = []
    for wname, fn in waves:
        for r in fn():
            if r.measured is None or float(r.measured) == 0:
                continue
            c, m = float(r.computed), float(r.measured)
            rel = abs(c - m) / abs(m) * 100
            rows.append({
                "wave": wname,
                "name": r.name,
                "formula": getattr(r, "formula_str", ""),
                "computed": c,
                "measured": m,
                "rel_err_pct": rel,
                "green_0_5": rel <= GREEN,
                "band_5": rel <= BAND_5,
            })

    n = len(rows)
    n5 = sum(1 for r in rows if r["band_5"])
    ng = sum(1 for r in rows if r["green_0_5"])
    errs = sorted(r["rel_err_pct"] for r in rows)
    med = errs[len(errs) // 2] if errs else None
    s_qm = domain_scalar("Quantum_Mechanics")
    s_qc = domain_scalar("Quantum_Computing")

    return {
        "panel": "qm_wave_field_of_use",
        "n_observables": n,
        "n_green_0_5": ng,
        "n_band_5": n5,
        "frac_green_0_5": ng / n if n else 0.0,
        "frac_band_5": n5 / n if n else 0.0,
        "median_rel_err_pct": med,
        "S_QM": s_qm,
        "S_QC": s_qc,
        "overall_ok": n5 == n and med is not None and med <= BAND_5,
        "worst": sorted(rows, key=lambda r: -r["rel_err_pct"])[:6],
        "instances": rows,
        "note": (
            "Pin seed formulas vs measured constants. "
            "Not a claim that FSOT replaces the Standard Model Lagrangian."
        ),
    }
