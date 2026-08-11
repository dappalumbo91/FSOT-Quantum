"""
Fold path v2 — chemistry folds + GPU fold queue + surface/phase folds.

python -m fsot_quantum.fold_v2
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.fold_gpu_queue import run_fold_gpu_queue_panel
from fsot_quantum.surface_phase_fold import run_surface_phase_fold_panel
from fsot_quantum.fold_jobs import run_fold_jobs_panel
from fsot_quantum.fold_complexity import cost_contrast


def main() -> int:
    t0 = time.perf_counter()
    chem = run_chemistry_fold_panel()
    gpuq = run_fold_gpu_queue_panel()
    surf = run_surface_phase_fold_panel()
    # keep v1 fold jobs green
    jobs = run_fold_jobs_panel()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "fold_v2_natural_steps",
        "pin": "D1D38A",
        "thesis": (
            "Next natural steps on fold path: chemistry residual folds, "
            "GPU fold job queue, surface+phase folds — still not Hilbert 2^n"
        ),
        "chemistry_fold": {
            "ok": chem["overall_ok"],
            "aspiration_0_5_ok": chem["aspiration_0_5_ok"],
            "green_base": f"{chem['n_green_0_5_base']}/{chem['n_observables']}",
            "green_fold": f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
            "median_fold_pct": chem["median_rel_err_fold_pct"],
            "rules": chem["rules_used"],
            "improved": len(chem.get("improved") or []),
        },
        "fold_gpu_queue": {
            "ok": gpuq["overall_ok"],
            "gpu": gpuq.get("gpu_name"),
            "highlights": gpuq.get("highlights"),
        },
        "surface_phase_fold": {
            "ok": surf["overall_ok"],
            "pass": f"{surf['pass_count']}/{surf['total']}",
            "ladder": surf["ladder"],
        },
        "fold_jobs_v1": {
            "ok": jobs["overall_ok"],
            "pass": f"{jobs['pass_count']}/{jobs['total']}",
        },
        "cost_contrast_n32": cost_contrast(32),
        "overall_ok": (
            chem["overall_ok"]
            and chem["aspiration_0_5_ok"]
            and gpuq["overall_ok"]
            and surf["overall_ok"]
            and jobs["overall_ok"]
        ),
        "wall_seconds": time.perf_counter() - t0,
        "now_implemented": [
            "chemistry formula-family fold: π⁵·φ → π⁵·φ+(π−θ_s) (0.5% aspiration)",
            "GPU fold queue: search/modular/Ising/pack/D_eff scalars",
            "surface bit+phase nested CSS folds d=3/5/7",
            "phase class via D_eff + surface distance (no QPE Hilbert)",
        ],
        "still_not_claimed": [
            "full molecular FCI/CASSCF",
            "device-scale FTQC thresholds",
            "RSA-scale factoring",
            "Hilbert-universal unitary simulation",
        ],
    }

    # Gate: if chemistry aspiration fails, overall fails (we require the step)
    # already included aspiration_0_5_ok in overall_ok

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "chemistry_fold.json").write_text(json.dumps(chem, indent=2), encoding="utf-8")
    (out / "fold_gpu_queue.json").write_text(json.dumps(gpuq, indent=2), encoding="utf-8")
    (out / "surface_phase_fold.json").write_text(json.dumps(surf, indent=2), encoding="utf-8")
    (out / "fold_v2.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Fold path v2 — natural steps",
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
        f"- **chemistry fold:** ok={report['chemistry_fold']['ok']} "
        f"0.5% base {report['chemistry_fold']['green_base']} → "
        f"fold {report['chemistry_fold']['green_fold']} "
        f"aspiration={report['chemistry_fold']['aspiration_0_5_ok']}",
        f"- **GPU fold queue:** ok={report['fold_gpu_queue']['ok']} "
        f"gpu={report['fold_gpu_queue']['gpu']} "
        f"highlights={report['fold_gpu_queue']['highlights']}",
        f"- **surface+phase folds:** {report['surface_phase_fold']['pass']} "
        f"ok={report['surface_phase_fold']['ok']}",
        f"- **fold jobs v1:** {report['fold_jobs_v1']['pass']} "
        f"ok={report['fold_jobs_v1']['ok']}",
        "",
        "## Cost contrast (n=32)",
        "",
        f"- Hilbert amps: `{report['cost_contrast_n32']['hilbert_amplitudes']}`",
        f"- Fold budget: `{report['cost_contrast_n32']['fold_probe_budget']}`",
        f"- Ratio: ~`{report['cost_contrast_n32']['ratio_hilbert_over_fold']:.0f}×`",
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
        "python -m fsot_quantum.fold_v2",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_V2.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_V2.md").write_text(text, encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
