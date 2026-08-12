"""
Field-of-use honesty suite — apply FSOT math to QM/QC jobs, label theater.

python -m fsot_quantum.field_of_use
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.fsot_field_opt import run_fsot_field_opt_panel
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.fold_jobs import fold_marked_search, fold_period_finding, fold_factor
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.domains import domain_scalar


# Honest classification — not marketing
JOB_LEDGER = [
    {
        "job": "chemistry observables",
        "industry": "quantum chemistry / FCI sales pitch",
        "fsot_math": "pin seed formulas + formula-family fold (π−θ_s)",
        "class": "applied_fsot",
        "not": "FCI / CASSCF",
    },
    {
        "job": "QM / SM constants (α, Weinberg, mass ratios)",
        "industry": "precision QM / particle data",
        "fsot_math": "vendor pin expressions vs measured",
        "class": "applied_fsot",
        "not": "replacing the Standard Model",
    },
    {
        "job": "marked search",
        "industry": "Grover",
        "fsot_math": "collapse through Θ on oracle field",
        "class": "applied_fsot",
        "not": "O(√N) query-complexity theorem",
    },
    {
        "job": "Ising / MaxCut",
        "industry": "QAOA / annealer",
        "fsot_math": "h_i=Σ J s_j → collapse + consensus + domain S",
        "class": "applied_fsot",
        "not": "QAOA circuit depth equivalence",
    },
    {
        "job": "period / factor (tiny N)",
        "industry": "Shor",
        "fsot_math": "modular order + collapse over candidate scores",
        "class": "applied_fsot",
        "not": "RSA-scale / Hilbert modular-exp",
    },
    {
        "job": "phase class",
        "industry": "QPE",
        "fsot_math": "S(D_eff) emergence/damping",
        "class": "applied_fsot",
        "not": "eigenphase of an arbitrary unitary",
    },
    {
        "job": "bit-reversal 'QFT-role'",
        "industry": "QFT",
        "fsot_math": "none — bit reverse is not a QFT",
        "class": "theater_do_not_claim",
        "not": "textbook QFT",
    },
    {
        "job": "Hilbert H/CX/QFT fragments",
        "industry": "circuit sim",
        "fsot_math": "seed π angles only; still 2^n amps",
        "class": "optional_bridge",
        "not": "the scaling law",
    },
]


def main() -> int:
    t0 = time.perf_counter()
    field_opt = run_fsot_field_opt_panel()
    qm = run_qm_wave_use_panel()
    chem = run_chemistry_fold_panel()
    gset = run_gset_official_panel()

    search = fold_marked_search(10_000, 4242)
    periods = [fold_period_finding(a, N) for a, N in ((7, 15), (5, 21), (2, 33))]
    factors = [fold_factor(N) for N in (15, 21, 33, 35)]

    s_qm = domain_scalar("Quantum_Mechanics")
    s_qc = domain_scalar("Quantum_Computing")

    jobs_ok = {
        "field_opt": field_opt["overall_ok"],
        "qm_waves": qm["overall_ok"],
        "chemistry_fold": chem["overall_ok"] and chem["aspiration_0_5_ok"],
        "gset_official": gset["overall_ok"],
        "search_collapse": bool(search.get("ok")),
        "period_fold": all(p.get("ok") for p in periods),
        "factor_fold": all(f.get("ok") for f in factors),
        "domain_signs": s_qm > 0 and s_qc < 0,
    }

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "field_of_use_honest",
        "pin": "D1D38A",
        "thesis": (
            "Apply FSOT mathematics (Θ collapse, consensus, D_eff / S, pin formulas) "
            "to QM/QC *jobs*. Label theater. Do not sell 2^n bridges as the path."
        ),
        "job_classification": JOB_LEDGER,
        "panels": {
            "field_opt": {
                "ok": field_opt["overall_ok"],
                "pass": f"{field_opt['pass_count']}/{field_opt['total']}",
                "exact": f"{field_opt['exact_hits']}/{field_opt['exact_total']}",
            },
            "qm_waves": {
                "ok": qm["overall_ok"],
                "green": f"{qm['n_green_0_5']}/{qm['n_observables']}",
                "band5": f"{qm['n_band_5']}/{qm['n_observables']}",
                "median_pct": qm["median_rel_err_pct"],
                "worst": qm["worst"][:3],
            },
            "chemistry": {
                "ok": chem["overall_ok"],
                "green_0_5": f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
            },
            "gset": {
                "ok": gset["overall_ok"],
                "status": gset["status"],
                "pass": f"{gset['pass_count']}/{gset['total']}",
            },
            "search": {"ok": search.get("ok"), "n": 10_000},
            "period": {
                "ok": all(p.get("ok") for p in periods),
                "pass": f"{sum(1 for p in periods if p.get('ok'))}/{len(periods)}",
            },
            "factor": {
                "ok": all(f.get("ok") for f in factors),
                "pass": f"{sum(1 for f in factors if f.get('ok'))}/{len(factors)}",
            },
            "S_QM": s_qm,
            "S_QC": s_qc,
        },
        "jobs_ok": jobs_ok,
        "overall_ok": all(jobs_ok.values()),
        "wall_seconds": time.perf_counter() - t0,
        "still_not_claimed": [
            "Hilbert-universal competitor to arbitrary QC circuits",
            "bit-reversal as QFT",
            "RSA-scale Shor",
            "FCI chemistry",
            "device-scale FTQC",
        ],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "fsot_field_opt.json").write_text(json.dumps(field_opt, indent=2), encoding="utf-8")
    (out / "qm_wave_use.json").write_text(json.dumps(qm, indent=2), encoding="utf-8")
    (out / "field_of_use.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Field of use — honest FSOT on QM/QC jobs",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        report["thesis"],
        "",
        "## Classification",
        "",
        "| Job | Industry pitch | FSOT math | Class |",
        "|-----|----------------|-----------|-------|",
    ]
    for j in JOB_LEDGER:
        md.append(
            f"| {j['job']} | {j['industry']} | {j['fsot_math']} | **{j['class']}** |"
        )
    md += [
        "",
        "## Live panels",
        "",
        f"- **field Ising/MaxCut:** {report['panels']['field_opt']['pass']} "
        f"exact {report['panels']['field_opt']['exact']}",
        f"- **QM pin waves:** green {report['panels']['qm_waves']['green']} "
        f"5% {report['panels']['qm_waves']['band5']} "
        f"median={report['panels']['qm_waves']['median_pct']}",
        f"- **chemistry fold:** {report['panels']['chemistry']['green_0_5']} @0.5%",
        f"- **Gset official:** {report['panels']['gset']['status']} "
        f"{report['panels']['gset']['pass']}",
        f"- **collapse search:** {report['panels']['search']['ok']}",
        f"- **period/factor:** {report['panels']['period']['pass']} / "
        f"{report['panels']['factor']['pass']}",
        f"- **S(QM), S(QC):** {s_qm:.4f}, {s_qc:.4f}",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.field_of_use",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FIELD_OF_USE.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FIELD_OF_USE.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "jobs_ok": jobs_ok,
        "field_opt": report["panels"]["field_opt"],
        "qm_waves": report["panels"]["qm_waves"],
        "chemistry": report["panels"]["chemistry"],
        "gset": report["panels"]["gset"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
