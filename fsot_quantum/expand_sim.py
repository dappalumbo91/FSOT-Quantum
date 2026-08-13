"""
Expand simulation: Lean chemistry + more quantum material records.

python -m fsot_quantum.expand_sim
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.lean_replay import replay_files
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


CHEM_FILES = (
    "chemical_structure_stability_panel_benchmark.json",
    "fuel_thermochemistry_public_anchors_benchmark.json",
    "maillard_chemistry_gap_fill_benchmark.json",
    "pubchem_stability_panel_benchmark.json",
    "chemical_engineering_extension_benchmark.json",
    "geochemistry_benchmark.json",
    "ionospheric_chemistry_coupling_benchmark.json",
    "pubchem_depth_open_benchmark.json",
)

QM_MORE = (
    "quantum_mechanics_gap_fill_benchmark.json",
    "quantum_optics_gap_fill_benchmark.json",
    "quantum_materials_benchmark.json",
    "founding_quantum_vacuum_panel_benchmark.json",
    "quantum_trinary_syntax_benchmark.json",
    "microtubule_quantum_consciousness_panel_benchmark.json",
)


def main() -> int:
    t0 = time.perf_counter()
    chem_pin = run_chemistry_fold_panel()
    qm_pin = run_qm_wave_use_panel()
    lean_chem = replay_files(CHEM_FILES)
    lean_qm = replay_files(QM_MORE)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "expand_sim",
        "pin": "D1D38A",
        "thesis": (
            "Pull solved Lean chemistry/QM atlas into this fold; "
            "keep pin chemistry 68/68; grow what we can simulate."
        ),
        "pin_chemistry": {
            "ok": chem_pin["overall_ok"] and chem_pin["aspiration_0_5_ok"],
            "green": f"{chem_pin['n_green_0_5_fold']}/{chem_pin['n_observables']}",
        },
        "pin_qm": {
            "ok": qm_pin["overall_ok"],
            "green": f"{qm_pin['n_green_0_5']}/{qm_pin['n_observables']}",
        },
        "lean_chemistry": {
            "ok": lean_chem.get("overall_ok"),
            "replayed": lean_chem.get("n_replayed"),
            "green": f"{lean_chem.get('n_green_0_5')}/{lean_chem.get('n_replayed')}",
            "band5": f"{lean_chem.get('n_band_5')}/{lean_chem.get('n_replayed')}",
            "worst": lean_chem.get("worst"),
        },
        "lean_qm_more": {
            "ok": lean_qm.get("overall_ok"),
            "replayed": lean_qm.get("n_replayed"),
            "green": f"{lean_qm.get('n_green_0_5')}/{lean_qm.get('n_replayed')}",
            "band5": f"{lean_qm.get('n_band_5')}/{lean_qm.get('n_replayed')}",
            "worst": lean_qm.get("worst"),
        },
        "overall_ok": (
            chem_pin["overall_ok"]
            and chem_pin["aspiration_0_5_ok"]
            and qm_pin["overall_ok"]
            and bool(lean_chem.get("overall_ok"))
            and bool(lean_qm.get("overall_ok"))
        ),
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "lean_chem_replay.json").write_text(json.dumps(lean_chem, indent=2), encoding="utf-8")
    (out / "lean_qm_more_replay.json").write_text(json.dumps(lean_qm, indent=2), encoding="utf-8")
    (out / "expand_sim.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Expand sim — Lean chemistry + more QM into this fold",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        f"- pin chemistry: {report['pin_chemistry']['green']}",
        f"- pin QM waves: {report['pin_qm']['green']}",
        f"- Lean chemistry replay: {report['lean_chemistry']['green']} @0.5% "
        f"({report['lean_chemistry']['replayed']} rows)",
        f"- Lean QM/optics/materials/vacuum: {report['lean_qm_more']['green']} "
        f"({report['lean_qm_more']['replayed']} rows)",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.expand_sim",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "EXPAND_SIM.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "EXPAND_SIM.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "pin_chemistry": report["pin_chemistry"],
        "lean_chemistry": report["lean_chemistry"],
        "lean_qm_more": report["lean_qm_more"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2, default=str))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
