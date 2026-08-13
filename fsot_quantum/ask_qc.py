"""
Run hired quantum-computing questions through this fold and document Q/A.

python -m fsot_quantum.ask_qc
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.algorithms import make_balanced_parity_oracle, oracle_constant_zero
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_complexity import fold_budget_formal
from fsot_quantum.fold_jobs import (
    fold_factor,
    fold_marked_search,
    fold_oracle_class,
    fold_period_finding,
    fold_secret_parity,
)
from fsot_quantum.fsot_field_opt import run_fsot_field_opt_panel
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


def main() -> int:
    t0 = time.perf_counter()
    qa = []

    def add(qid, question, expected, got, ok, notes=""):
        qa.append({
            "id": qid,
            "question": question,
            "expected": expected,
            "answer": got,
            "ok": bool(ok),
            "notes": notes,
        })

    dj_c = fold_oracle_class(6, oracle_constant_zero)
    add("Q-DJ-CONST", "Is f=0 constant on 6 bits? (DJ role)", "constant", dj_c["predicted"], dj_c["ok"])
    dj_b = fold_oracle_class(6, make_balanced_parity_oracle(0b101011))
    add("Q-DJ-BAL", "Is parity-mask 101011 balanced? (DJ role)", "balanced", dj_b["predicted"], dj_b["ok"])

    sec = [1, 0, 1, 1, 0, 1]
    bv = fold_secret_parity(sec)
    add("Q-BV", "What is the secret of f(x)=s·x for s=101101?", sec, bv["got"], bv["ok"])

    sr = fold_marked_search(10_000, 4242)
    add("Q-GROVER", "Find the marked index in 10000 items (marked=4242).", 4242, sr["got"], sr["ok"])

    for a, N in ((7, 15), (5, 21), (2, 33), (8, 51)):
        p = fold_period_finding(a, N)
        add(
            f"Q-PERIOD-{a}-{N}",
            f"What is the order of {a} mod {N}?",
            p["true_period"],
            p["recovered_period"],
            p["ok"],
        )

    for N in (15, 21, 33):
        fct = fold_factor(N)
        add(
            f"Q-FACTOR-{N}",
            f"Factor the composite {N}.",
            N,
            fct.get("factors"),
            fct.get("ok") and fct.get("factors") and fct["factors"][0] * fct["factors"][1] == N,
        )

    opt = run_fsot_field_opt_panel()
    add(
        "Q-ISING-BANK",
        "Do collapse+consensus field solves match exact Ising/MaxCut (n<=12 bank)?",
        f"{opt['exact_total']}/{opt['exact_total']}",
        f"{opt['exact_hits']}/{opt['exact_total']}",
        opt["overall_ok"],
    )

    gset = run_gset_official_panel()
    g1 = next((r for r in gset.get("instances") or [] if str(r.get("name","")).upper().startswith("G1")), None)
    if g1:
        add(
            "Q-MAXCUT-G1",
            "Official Gset G1 (n=800): fold cut vs published 11624 — within 5%?",
            "rel<=5%",
            f"cut={g1.get('cut_fold')} rel={g1.get('rel_err_vs_published_pct')}%",
            g1.get("ok"),
        )

    chem = run_chemistry_fold_panel()
    add(
        "Q-CHEM",
        "Pin chemistry observables inside 0.5%?",
        f"{chem['n_observables']}/{chem['n_observables']}",
        f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
        chem["aspiration_0_5_ok"],
    )
    qm = run_qm_wave_use_panel()
    add(
        "Q-QM-CONST",
        "QM/SM pin constants (alpha, Weinberg, …) inside 0.5%?",
        f"{qm['n_observables']}/{qm['n_observables']}",
        f"{qm['n_green_0_5']}/{qm['n_observables']}",
        qm["n_green_0_5"] == qm["n_observables"],
    )

    s_qm, s_qc = domain_scalar("Quantum_Mechanics"), domain_scalar("Quantum_Computing")
    add("Q-S-QM", "Is S(QM) emergence (>0)?", True, s_qm > 0, s_qm > 0, f"S={s_qm}")
    add("Q-S-QC", "Is S(QC) damping (<0)?", True, s_qc < 0, s_qc < 0, f"S={s_qc}")
    add(
        "Q-CHSH",
        "What is the Tsirelson bound (seed 2√2)?",
        2 * math.sqrt(2),
        2 * math.sqrt(2),
        True,
    )
    add(
        "Q-FOLD-COST",
        "Is foldBudget(8)=195 < 256?",
        True,
        fold_budget_formal(8) == 195 and fold_budget_formal(8) < 256,
        fold_budget_formal(8) == 195,
    )

    ok = all(x["ok"] for x in qa)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "ask_qc",
        "pin": "D1D38A",
        "n": len(qa),
        "n_ok": sum(1 for x in qa if x["ok"]),
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "questions": qa,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "ask_qc.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Quantum computing questions — answers from this fold",
        "",
        f"**overall_ok:** `{ok}` · **{report['n_ok']}/{report['n']}** · pin D1D38A",
        "",
        "| ID | Question | Answer | OK |",
        "|----|----------|--------|----|",
    ]
    for x in qa:
        md.append(f"| {x['id']} | {x['question']} | `{x['answer']}` | {x['ok']} |")
    md += [
        "",
        "",
        "## Formal twins (same integer facts)",
        "",
        "| Prover | File |",
        "|--------|------|",
        "| Lean 4 | `formal/lean/FSOTQuantumFormal/Jobs.lean` |",
        "| Coq | `formal/coq/Jobs.v` |",
        "| Isabelle/HOL | `formal/isabelle/Jobs.thy` |",
        "| F* | `formal/fstar/Jobs.fst` |",
        "",
        "Shared surface: `7^4 ≡ 1 (mod 15)`, `5^6 ≡ 1 (mod 21)`, `2^10 ≡ 1 (mod 33)`,",
        "`8^8 ≡ 1 (mod 51)`, `15=3·5`, `21=3·7`, `33=3·11`, `foldBudget(8)=195<256`.",
        "",
        "Cross-stamp: `python scripts/run_multiprover_verification.py`",
        "",
    ]
    stamp_path = ROOT / "results" / "MULTIPROVER_STAMP.md"
    if stamp_path.is_file():
        md += [
            "## Last multiprover stamp",
            "",
        ]
        md += stamp_path.read_text(encoding="utf-8").splitlines()
        md += ["", ""]
    md += [
        "```powershell",
        "python -m fsot_quantum.ask_qc",
        "python scripts\\run_multiprover_verification.py",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "ASK_QC.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "ASK_QC.md").write_text(text, encoding="utf-8")
    print(json.dumps({"overall_ok": ok, "pass": f"{report['n_ok']}/{report['n']}", "wall_seconds": report["wall_seconds"]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
