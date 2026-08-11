"""
Fold path v3 — benchmarks, multi-stream scheduler, lattice surgery, chem catalog.

python -m fsot_quantum.fold_v3
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.fold_benchmarks import run_fold_benchmarks_panel
from fsot_quantum.fold_scheduler import run_fold_scheduler_panel
from fsot_quantum.lattice_surgery_fold import run_lattice_surgery_fold_panel
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.fold_complexity import cost_contrast


def main() -> int:
    t0 = time.perf_counter()
    bench = run_fold_benchmarks_panel()
    sched = run_fold_scheduler_panel()
    surgery = run_lattice_surgery_fold_panel()
    chem = run_chemistry_fold_panel()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "fold_v3_natural_steps",
        "pin": "D1D38A",
        "thesis": (
            "Fold path v3: public MaxCut/Ising under cost ledger, multi-stream "
            "fold scheduler, lattice-surgery logical folds, broader chem catalog"
        ),
        "fold_benchmarks": {
            "ok": bench["overall_ok"],
            "pass": f"{bench['pass_count']}/{bench['total']}",
            "summary": bench["summary"],
        },
        "fold_scheduler": {
            "ok": sched["overall_ok"],
            "gpu": sched.get("gpu_name"),
            "serial_s": sched["serial"]["wall_seconds"],
            "streamed_s": sched["streamed"]["wall_seconds"],
            "speedup": sched["speedup_serial_over_streamed"],
            "mode": sched["streamed"]["mode"],
        },
        "lattice_surgery_fold": {
            "ok": surgery["overall_ok"],
            "pass": f"{surgery['pass_count']}/{surgery['total']}",
            "ladder": surgery["ladder"],
        },
        "chemistry_fold": {
            "ok": chem["overall_ok"],
            "aspiration_0_5_ok": chem["aspiration_0_5_ok"],
            "green_fold": f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
            "n_families": chem.get("n_families"),
            "catalog": chem.get("formula_family_catalog"),
        },
        "cost_contrast_n24": cost_contrast(24),
        "overall_ok": (
            bench["overall_ok"]
            and sched["overall_ok"]
            and surgery["overall_ok"]
            and chem["overall_ok"]
            and chem["aspiration_0_5_ok"]
        ),
        "wall_seconds": time.perf_counter() - t0,
        "now_implemented": [
            "MaxCut/Ising fold benchmarks + Hilbert-vs-fold cost ledger",
            "multi-stream CUDA fold scheduler (search/Ising/pack/scalar)",
            "lattice-surgery merge/split/CNOT/ZZ folds d=3/5/7",
            "broader chemistry formula-family catalog + 0.5% green held",
        ],
        "still_not_claimed": [
            "continuum FTQC lattice-surgery thresholds",
            "QAOA circuit-depth equivalence",
            "RSA-scale factoring",
            "full FCI/CASSCF chemistry",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "fold_benchmarks.json").write_text(json.dumps(bench, indent=2), encoding="utf-8")
    (out / "fold_scheduler.json").write_text(json.dumps(sched, indent=2), encoding="utf-8")
    (out / "lattice_surgery_fold.json").write_text(
        json.dumps(surgery, indent=2), encoding="utf-8"
    )
    (out / "chemistry_fold.json").write_text(json.dumps(chem, indent=2), encoding="utf-8")
    (out / "fold_v3.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Fold path v3 — natural steps",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        "## Thesis",
        "",
        report["thesis"],
        "",
        "## Panels",
        "",
        f"- **fold benchmarks:** {report['fold_benchmarks']['pass']} "
        f"ok={report['fold_benchmarks']['ok']} summary={report['fold_benchmarks']['summary']}",
        f"- **fold scheduler:** ok={report['fold_scheduler']['ok']} "
        f"serial={report['fold_scheduler']['serial_s']:.3f}s "
        f"streamed={report['fold_scheduler']['streamed_s']:.3f}s "
        f"speedup={report['fold_scheduler']['speedup']}",
        f"- **lattice surgery folds:** {report['lattice_surgery_fold']['pass']} "
        f"ok={report['lattice_surgery_fold']['ok']}",
        f"- **chemistry catalog:** green={report['chemistry_fold']['green_fold']} "
        f"families={report['chemistry_fold']['n_families']} "
        f"aspiration={report['chemistry_fold']['aspiration_0_5_ok']}",
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
        "python -m fsot_quantum.fold_v3",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_V3.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_V3.md").write_text(text, encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
