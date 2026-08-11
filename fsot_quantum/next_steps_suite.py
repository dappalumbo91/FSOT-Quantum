"""
Next natural steps suite: large Hilbert circuits · stronger codes · modular Shor · chemistry strict.

Writes results/next_steps_suite.json
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.circuit_library import run_circuit_library_panel
from fsot_quantum.logical_codes import run_stronger_codes_panel
from fsot_quantum.shor_modular import run_shor_modular_panel
from fsot_quantum.chemistry_strict import run_chemistry_strict_panel
from fsot_quantum.compete_qm_qc import run_compete_qm_qc
from fsot_quantum.gpu_parallel import prefer_device


def run_next_steps() -> dict:
    t0 = time.perf_counter()
    lib = run_circuit_library_panel()
    codes = run_stronger_codes_panel()
    shor = run_shor_modular_panel()
    chem = run_chemistry_strict_panel()
    base = run_compete_qm_qc()

    panels = {
        "circuit_library_n8_12": {
            "ok": lib["overall_ok"],
            "pass": f"{lib['pass_count']}/{lib['total']}",
        },
        "stronger_logical_codes": {
            "ok": codes["overall_ok"],
            "ladder": codes["ladder"],
            "pass": f"{codes['pass_count']}/{codes['total']}",
        },
        "shor_full_modular": {
            "ok": shor["overall_ok"],
            "pass": f"{shor['pass_count']}/{shor['total']}",
            "cases": [
                {
                    "a": c["a"],
                    "N": c["N"],
                    "r": c["true_period"],
                    "hat": c["recovered_period"],
                    "ok": c["ok"],
                    "n_qubits": c["n_qubits"],
                }
                for c in shor["cases"]
            ],
        },
        "chemistry_strict": {
            "ok": chem["overall_ok"],
            "median_pct": chem["median_rel_err_pct"],
            "frac_0_5": chem["frac_green_0_5"],
            "frac_5": chem["frac_band_5"],
            "aspiration_0_5": chem["aspiration_0_5_ok"],
        },
        "compete_qm_qc_base": {"ok": base["overall_ok"]},
    }

    # Gate: library, codes, shor modular, base compete required;
    # chemistry_strict ok is all within 5%; 0.5% is aspiration metric
    overall = all(
        panels[k]["ok"]
        for k in (
            "circuit_library_n8_12",
            "stronger_logical_codes",
            "shor_full_modular",
            "chemistry_strict",
            "compete_qm_qc_base",
        )
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "next_steps_natural",
        "device": prefer_device(),
        "panels": panels,
        "full": {
            "circuit_library": lib,
            "logical_codes": codes,
            "shor_modular": shor,
            "chemistry_strict": chem,
        },
        "overall_ok": overall,
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "next_steps_suite.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out / "circuit_library.json").write_text(json.dumps(lib, indent=2), encoding="utf-8")
    (out / "logical_codes.json").write_text(json.dumps(codes, indent=2), encoding="utf-8")
    (out / "shor_modular.json").write_text(json.dumps(shor, indent=2), encoding="utf-8")

    md = [
        "# Next natural steps suite",
        "",
        f"**overall_ok:** `{overall}`",
        f"**device:** `{report['device']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        "| Panel | OK | Detail |",
        "|-------|----|--------|",
    ]
    for k, v in panels.items():
        md.append(f"| {k} | {v.get('ok')} | `{v}` |")
    (out / "NEXT_STEPS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (ROOT / "docs" / "NEXT_STEPS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


def main() -> int:
    r = run_next_steps()
    print(json.dumps({
        "overall_ok": r["overall_ok"],
        "panels": r["panels"],
        "wall_seconds": r["wall_seconds"],
    }, indent=2))
    return 0 if r["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
