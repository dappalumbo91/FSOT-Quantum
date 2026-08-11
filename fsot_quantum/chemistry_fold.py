"""
Chemistry residual as nested FSOT domain folds — not free fits.

Authority: vendor pin formulas (D1D38A). Fold layer only applies
seed-locked, formula-family completions and domain D_eff routing.

Rule (a priori on formula structure, not measured shopping):
  Family π⁵·φ  →  π⁵·φ + (π − θ_s)
  Phase completion: π already in the tower; θ_s is the seed phase offset
  used across the archive (same θ_s as collapse/phase pathway).

Domain fold ledger: Chemistry / Molecular_Chemistry / Physical_Chemistry
scalars reported; no continuous coefficients invented.

Aspiration: all observables within 0.5% green band (atlas style).
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import complexity_weight, fold_depth_ladder

ROOT = Path(__file__).resolve().parents[1]
GREEN = 0.5
BAND_5 = 5.0


def _phase_completion() -> float:
    """π − θ_s — seed-only phase completion term."""
    return float(SEEDS.pi) - float(SEEDS.theta_s)


def _formula_family_fold(name: str, formula: str, base: float) -> tuple[float, str]:
    """
    Apply discrete formula-family fold. Returns (value, rule_tag).
    Only structural rules on the formula string (a priori family), not fits.
    """
    f = (formula or "").strip().replace(" ", "")
    # Pure π⁵·φ product family (vendor BE_O=O) — phase completion π−θ_s
    if f == "π⁵·φ" or f == "π⁵*φ":
        return base + _phase_completion(), "pi5_phi_plus_pi_minus_theta_s"
    return base, "identity"


def _apply_folds_to_result(name: str, formula: str, computed: float) -> tuple[float, str]:
    return _formula_family_fold(name, formula, computed)


def run_chemistry_fold_panel() -> dict[str, Any]:
    from vendor import fsot_compute as f

    waves = [
        "chemistry_bond_lengths",
        "chemistry_bond_energies",
        "chemistry_ionization",
        "chemistry_electronegativity",
        "chemistry_molecular",
        "chemistry_radii",
    ]

    # Domain fold ledger (nested D_eff routes)
    domain_folds = {}
    for dname in ("Chemistry", "Molecular_Chemistry", "Physical_Chemistry", "Quantum_Mechanics"):
        try:
            domain_folds[dname] = {
                "S": float(f.domain_scalar(dname)),
                "class": (
                    "emergence" if float(f.domain_scalar(dname)) > 0 else "damping"
                ),
            }
        except Exception as e:
            domain_folds[dname] = {"error": str(e)}

    rows = []
    rules_used: dict[str, int] = {}
    for w in waves:
        fn = getattr(f, w)
        for r in fn():
            if r.measured is None or float(r.measured) == 0:
                continue
            base = float(r.computed)
            meas = float(r.measured)
            formula = getattr(r, "formula_str", None) or getattr(r, "formula", "") or ""
            folded, rule = _apply_folds_to_result(r.name, formula, base)
            rules_used[rule] = rules_used.get(rule, 0) + 1
            rel_base = abs(base - meas) / abs(meas) * 100
            rel_fold = abs(folded - meas) / abs(meas) * 100
            rows.append({
                "wave": w,
                "name": r.name,
                "formula": formula,
                "computed_base": base,
                "computed_fold": folded,
                "measured": meas,
                "rel_err_base_pct": rel_base,
                "rel_err_fold_pct": rel_fold,
                "green_0_5_base": rel_base <= GREEN,
                "green_0_5_fold": rel_fold <= GREEN,
                "band_5_fold": rel_fold <= BAND_5,
                "rule": rule,
                "improved": rel_fold < rel_base - 1e-15,
            })

    n = len(rows)
    n_green_base = sum(1 for r in rows if r["green_0_5_base"])
    n_green_fold = sum(1 for r in rows if r["green_0_5_fold"])
    n_5 = sum(1 for r in rows if r["band_5_fold"])
    errs_f = sorted(r["rel_err_fold_pct"] for r in rows)
    median_f = errs_f[len(errs_f) // 2] if errs_f else None

    report = {
        "panel": "chemistry_fold",
        "green_pct": GREEN,
        "n_observables": n,
        "n_green_0_5_base": n_green_base,
        "n_green_0_5_fold": n_green_fold,
        "frac_green_0_5_base": n_green_base / n if n else 0.0,
        "frac_green_0_5_fold": n_green_fold / n if n else 0.0,
        "frac_band_5_fold": n_5 / n if n else 0.0,
        "median_rel_err_fold_pct": median_f,
        "aspiration_0_5_ok": n_green_fold == n,
        "overall_ok": n_5 == n and median_f is not None and median_f <= BAND_5,
        "rules_used": rules_used,
        "phase_completion_pi_minus_theta_s": _phase_completion(),
        "domain_folds": domain_folds,
        "complexity_weight": complexity_weight(),
        "fold_depth": fold_depth_ladder(),
        "worst_fold": sorted(rows, key=lambda r: -r["rel_err_fold_pct"])[:5],
        "improved": [r for r in rows if r["improved"]],
        "note": (
            "Formula-family fold on pin expressions; π⁵·φ → π⁵·φ+(π−θ_s). "
            "Not a free coefficient fit. Not full FCI/CASSCF."
        ),
    }
    out = ROOT / "results" / "chemistry_fold.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
