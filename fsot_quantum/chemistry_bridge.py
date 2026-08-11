"""
Chemistry residual bridge — FSOT domain Chemistry + vendor seed formulas.

Uses vendor/fsot_compute chemistry_* waves (zero free params) and domain S.
Not full CI / quantum chemistry FCI — residual gate on seed-derived observables.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import domain_scalar

ROOT = Path(__file__).resolve().parents[1]


def run_chemistry_residual_panel() -> dict[str, Any]:
    from vendor import fsot_compute as f

    rows = []
    for fn_name in (
        "chemistry_bond_lengths",
        "chemistry_bond_energies",
        "chemistry_ionization",
        "chemistry_molecular",
    ):
        fn = getattr(f, fn_name)
        results = fn()
        errs = []
        n_ok = 0
        n = 0
        for r in results:
            if r.measured is None or r.measured == 0:
                continue
            n += 1
            rel = abs(float(r.computed - r.measured) / float(r.measured)) * 100
            errs.append(rel)
            if rel < 5.0:  # same band as vendor report "within 5%"
                n_ok += 1
        med = sorted(errs)[len(errs) // 2] if errs else None
        rows.append({
            "wave": fn_name,
            "n": n,
            "within_5pct": n_ok,
            "median_rel_err_pct": med,
            "ok": med is not None and med <= 5.0,
        })

    s_chem = float(f.domain_scalar("Chemistry"))
    s_qm = float(f.domain_scalar("Quantum_Mechanics"))
    report = {
        "panel": "chemistry_residual_bridge",
        "S_Chemistry": s_chem,
        "S_Quantum_Mechanics": s_qm,
        "waves": rows,
        "overall_ok": all(r["ok"] for r in rows if r["n"] > 0),
        "note": (
            "Seed-formula residuals from vendor chemistry waves; "
            "not full many-body quantum chemistry simulation."
        ),
        "seeds_pin": "D1D38A",
    }
    out = ROOT / "results" / "chemistry_bridge.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
