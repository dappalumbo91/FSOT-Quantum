"""
Compete suite: Hilbert universality fragment · logical qubits · QFT/Shor · chemistry.

Addresses the gap list: Hilbert unitaries, logical encoding, QFT/Shor structure,
chemistry residuals — still zero free parameters, pin D1D38A.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.hilbert import gate_set_fidelity_selftest, ANGLES
from fsot_quantum.logical import logical_error_correction_selftest, logical_distance
from fsot_quantum.qft_shor import qft_selftest, shor_bank_selftest
from fsot_quantum.chemistry_bridge import run_chemistry_residual_panel
from fsot_quantum.gpu_parallel import prefer_device


def run_compete_qm_qc() -> dict:
    t0 = time.perf_counter()
    hilbert = gate_set_fidelity_selftest()
    logical = logical_error_correction_selftest()
    qft = qft_selftest()
    shor = shor_bank_selftest()
    chem = run_chemistry_residual_panel()

    panels = {
        "hilbert_universal_fragment": {
            "ok": hilbert["ok"],
            "bell_fidelity": hilbert["bell_fidelity"],
            "ghz_ok": hilbert["ghz_ok"],
            "seed_angles": hilbert["angles_seed_only"],
        },
        "logical_qubits": {
            "ok": logical["ok"],
            "distance": logical["distance"],
            "single_error_correct": logical["single_error_correct"],
        },
        "qft": {
            "ok": qft["ok"],
            "uniform_on_zero": qft["qft_uniform_on_zero"],
            "iqft_fidelity": qft["iqft_roundtrip_fidelity"],
        },
        "shor_period_tiny": {
            "ok": shor["ok"],
            "pass": f"{shor['n_pass']}/{shor['n_total']}",
            "cases": [
                {
                    "a": c["a"],
                    "N": c["N"],
                    "true_r": c["true_period"],
                    "recovered_r": c["recovered_period"],
                    "ok": c["ok"],
                }
                for c in shor["cases"]
            ],
        },
        "chemistry_residual": {
            "ok": chem["overall_ok"],
            "S_Chemistry": chem["S_Chemistry"],
            "waves": chem["waves"],
        },
    }

    overall = all(p["ok"] for p in panels.values())
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "compete_qm_qc",
        "goal": (
            "Extend FSOT-QC toward Hilbert unitaries, logical encoding, "
            "QFT/Shor structure, chemistry residuals — zero free params"
        ),
        "device": prefer_device(),
        "pin": "D1D38A",
        "panels": panels,
        "overall_ok": overall,
        "wall_seconds": time.perf_counter() - t0,
        "still_not_claimed": [
            "cryptographically large Shor",
            "surface-code FTQC thresholds",
            "full molecular FCI / CASSCF",
            "device-independent quantum supremacy",
        ],
        "now_implemented": [
            "complex statevector + H/X/Y/Z/S/T/CNOT/CPhase (seed angles)",
            f"logical repetition code d={logical_distance()}",
            "QFT + IQFT roundtrip; tiny Shor CF recovery N=15,21",
            "vendor chemistry wave residual bridge",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "compete_qm_qc.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Compete QM/QC suite",
        "",
        f"**overall_ok:** `{overall}`",
        f"**device:** `{report['device']}`",
        "",
        "## Panels",
        "",
        "| Panel | OK | Detail |",
        "|-------|----|--------|",
        f"| Hilbert universal fragment | {panels['hilbert_universal_fragment']['ok']} | Bell F={panels['hilbert_universal_fragment']['bell_fidelity']:.6f} |",
        f"| Logical qubits | {panels['logical_qubits']['ok']} | d={panels['logical_qubits']['distance']} |",
        f"| QFT | {panels['qft']['ok']} | IQFT F={panels['qft']['iqft_fidelity']:.6f} |",
        f"| Shor tiny | {panels['shor_period_tiny']['ok']} | {panels['shor_period_tiny']['pass']} |",
        f"| Chemistry residual | {panels['chemistry_residual']['ok']} | S_chem={panels['chemistry_residual']['S_Chemistry']:.4f} |",
        "",
        "## Now implemented",
        "",
    ]
    for x in report["now_implemented"]:
        md.append(f"- {x}")
    md += ["", "## Still not claimed", ""]
    for x in report["still_not_claimed"]:
        md.append(f"- {x}")
    md += [
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.compete_qm_qc",
        "```",
        "",
    ]
    (out / "COMPETE_QM_QC.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / "docs" / "COMPETE_QM_QC.md").write_text("\n".join(md), encoding="utf-8")
    return report


def main() -> int:
    r = run_compete_qm_qc()
    print(json.dumps({
        "overall_ok": r["overall_ok"],
        "panels": {k: v.get("ok") for k, v in r["panels"].items()},
        "shor": r["panels"]["shor_period_tiny"],
        "hilbert_bell_F": r["panels"]["hilbert_universal_fragment"]["bell_fidelity"],
        "wall_seconds": r["wall_seconds"],
    }, indent=2))
    return 0 if r["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
