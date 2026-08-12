"""
QC / QM accuracy board — hired jobs, FSOT math, no cryogenic apparatus.

python -m fsot_quantum.qc_accuracy
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
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel
from fsot_quantum.fsot_field_opt import run_fsot_field_opt_panel
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.fold_jobs import (
    fold_factor,
    fold_marked_search,
    fold_period_finding,
    fold_oracle_class,
    fold_secret_parity,
)
from fsot_quantum.algorithms import make_balanced_parity_oracle, oracle_constant_zero
from fsot_quantum.entangle_qi_jobs import run_entangle_qi_panel
from fsot_quantum.domains import domain_scalar


def main() -> int:
    t0 = time.perf_counter()
    chem = run_chemistry_fold_panel()
    qm = run_qm_wave_use_panel()
    opt = run_fsot_field_opt_panel()
    gset = run_gset_official_panel()
    qi = run_entangle_qi_panel()

    dj = fold_oracle_class(8, make_balanced_parity_oracle(0b10110011))
    dj0 = fold_oracle_class(8, oracle_constant_zero)
    bv = fold_secret_parity([1, 0, 1, 1, 0, 1, 0, 1])
    search = fold_marked_search(50_000, 4242)
    periods = [fold_period_finding(a, N) for a, N in ((7, 15), (5, 21), (2, 33), (8, 51))]
    factors = [fold_factor(N) for N in (15, 21, 33, 35, 51)]

    g1 = None
    for r in gset.get("instances") or []:
        if str(r.get("name", "")).upper().startswith("G1"):
            g1 = r
            break

    jobs = {
        "chemistry_0_5": chem["aspiration_0_5_ok"],
        "qm_waves_0_5": qm["n_green_0_5"] == qm["n_observables"],
        "field_opt_exact": opt["exact_hits"] == opt["exact_total"] and opt["overall_ok"],
        "gset_g1": bool(gset["overall_ok"] and g1 and g1.get("ok")),
        "dj": bool(dj.get("ok") and dj0.get("ok")),
        "bv": bool(bv.get("ok")),
        "search": bool(search.get("ok")),
        "period": all(p.get("ok") for p in periods),
        "factor": all(f.get("ok") for f in factors),
        "entangle_qi": bool(qi.get("overall_ok")),
        "domain_signs": domain_scalar("Quantum_Mechanics") > 0
        and domain_scalar("Quantum_Computing") < 0,
    }

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "qc_accuracy",
        "pin": "D1D38A",
        "goal": (
            "Same QC/QM jobs, FSOT math on ordinary hardware — "
            "not a dilution fridge. Accuracy ledger only."
        ),
        "jobs_ok": jobs,
        "detail": {
            "chemistry": f"{chem['n_green_0_5_fold']}/{chem['n_observables']} @0.5% "
            f"median={chem['median_rel_err_fold_pct']}",
            "qm_waves": f"{qm['n_green_0_5']}/{qm['n_observables']} @0.5% "
            f"median={qm['median_rel_err_pct']}",
            "field_opt": f"{opt['exact_hits']}/{opt['exact_total']} exact",
            "g1_rel_pct_vs_bks": (g1 or {}).get("rel_err_vs_published_pct"),
            "g1_cut": (g1 or {}).get("cut_fold"),
            "period": f"{sum(1 for p in periods if p.get('ok'))}/{len(periods)}",
            "factor": f"{sum(1 for f in factors if f.get('ok'))}/{len(factors)}",
            "entangle_qi": f"{qi.get('n_green_0_5')}/{qi.get('n_replayed')}",
        },
        "overall_ok": all(jobs.values()),
        "wall_seconds": time.perf_counter() - t0,
        "not_this_program": [
            "cryogenic QPU design",
            "LLM free-parameter substrate",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "qc_accuracy.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# QC / QM accuracy — math path, not a fridge",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        report["goal"],
        "",
        "| Job | OK | Detail |",
        "|-----|----|--------|",
    ]
    labels = {
        "chemistry_0_5": "chemistry pin @0.5%",
        "qm_waves_0_5": "QM / SM constants @0.5%",
        "field_opt_exact": "Ising/MaxCut field exact",
        "gset_g1": "official G1 vs published BKS",
        "dj": "oracle class (DJ role)",
        "bv": "secret parity (BV role)",
        "search": "marked search (Grover role)",
        "period": "period finding (Shor core)",
        "factor": "factor (Shor end job)",
        "entangle_qi": "Lean entanglement / QI / math",
        "domain_signs": "S(QM)>0, S(QC)<0",
    }
    for k, lab in labels.items():
        md.append(f"| {lab} | {jobs[k]} | {report['detail'].get(k, '')} |")
    md += [
        "",
        f"- G1 cut `{report['detail']['g1_cut']}` · rel vs 11624 "
        f"`{report['detail']['g1_rel_pct_vs_bks']}%`",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.qc_accuracy",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "QC_ACCURACY.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "QC_ACCURACY.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "jobs_ok": jobs,
        "detail": report["detail"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
