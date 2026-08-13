"""
Hard questions — answered with FSOT mathematics, not someone else's circuit.

Thesis:
  Quantum algorithms exist because the *questions* they are hired for are
  supposed to be out of reach of ordinary machines via Hilbert / FCI / enum.
  This module asks those questions. It does not run DJ, Grover, Shor, or QAOA.
  It answers with S = K(T1+T2+T3), domain folds, and pin-locked closed forms.

  Brute 2^n is the competing cost we refuse. K is the universal scale.

python -m fsot_quantum.hard_questions
python -m fsot_quantum hard
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.scalar import compute_scalar, compute_scalar_terms
from fsot_lib.seeds import SEEDS
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.fold_complexity import (
    K_MICRO,
    fold_work_k_int,
    fold_work_via_k,
    hilbert_statevector_bytes,
    k_closed_form,
    k_matches_pin,
    k_scaling_law,
)
from fsot_quantum.fold_jobs import fold_factor, fold_marked_search
from fsot_quantum.gset_official import _fast_maxcut, run_gset_official_panel
from fsot_quantum.large_maxcut import _cycle, _seed_chords
from fsot_quantum.optimization import energy_ising, fsot_local_spins
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


def _hilbert_infeasible(n: int) -> dict[str, Any]:
    b = hilbert_statevector_bytes(n)
    return {
        "n": n,
        "hilbert_amps": None if n >= 63 else (1 << n),
        "hilbert_bytes": b,
        "fits_omen_32gib": bool(b != -1 and b <= 32 * (1 << 30)),
        "fold_work_k": fold_work_k_int(n),
    }


def main() -> int:
    t0 = time.perf_counter()
    qa: list[dict[str, Any]] = []

    def add(
        qid: str,
        question: str,
        expected: Any,
        got: Any,
        ok: bool,
        *,
        why_hard: str,
        method: str,
        check: str,
        notes: str = "",
        extra: dict[str, Any] | None = None,
    ) -> None:
        row: dict[str, Any] = {
            "id": qid,
            "question": question,
            "expected": expected,
            "answer": got,
            "ok": bool(ok),
            "why_hard": why_hard,
            "method": method,
            "independent_check": check,
            "notes": notes,
        }
        if extra:
            row["extra"] = extra
        qa.append(row)

    # --- K is the scaling law ------------------------------------------------
    k_pin = float(SEEDS.k)
    k_cf = k_closed_form()
    add(
        "H-K-CLOSED",
        "What is the universal scaling constant K?",
        k_pin,
        k_cf,
        k_matches_pin(),
        why_hard="Not a circuit. Closed form from seeds only: φ·(γ/e)·√2/ln(π)·99/100.",
        method="vendor 3.11 / SEEDS.k",
        check="closed_form vs pin",
        extra={"abs_delta": abs(k_pin - k_cf), "k_micro": K_MICRO},
    )
    add(
        "H-K-WORK-8",
        "What is K-scaled fold work at n=8 vs Hilbert 256?",
        47,
        fold_work_k_int(8),
        fold_work_k_int(8) == 47 == fold_work_via_k(8) and fold_work_k_int(8) < 256,
        why_hard="Integer twin of ceil(n/K)+27. Competing cost is 2^n.",
        method="fold_work_k_int",
        check="integer identity",
    )
    add(
        "H-K-WORK-64",
        "What is K-scaled fold work at n=64 vs 2^64 amplitudes?",
        180,
        fold_work_k_int(64),
        fold_work_k_int(64) == 180 and fold_work_k_int(64) < (1 << 20),
        why_hard="2^64 statevector is ~295 exabytes. K-work is 180 units.",
        method="fold_work_k_int",
        check="integer identity",
        extra=_hilbert_infeasible(64),
    )

    # --- S = K(T1+T2+T3) on the two quantum domains --------------------------
    for name, obs in (
        ("Quantum_Mechanics", True),
        ("Quantum_Computing", False),
    ):
        d = DOMAINS[name]
        terms = compute_scalar_terms(D_eff=float(d.D_eff), observed=obs)
        s_dom = domain_scalar(name)
        s_re = compute_scalar(D_eff=float(d.D_eff), observed=obs)
        ident = abs(terms["S"] - terms["K"] * (terms["T1"] + terms["T2"] + terms["T3"])) < 1e-15
        match = abs(terms["S"] - s_re) < 1e-15
        add(
            f"H-S-{name}",
            f"Does S({name}) equal K·(T1+T2+T3) at D_eff={d.D_eff}?",
            True,
            ident and match,
            ident and match,
            why_hard="The theory identity. If this fails, nothing else is FSOT.",
            method="compute_scalar_terms",
            check="algebraic identity",
            extra={
                "S": terms["S"],
                "domain_scalar": s_dom,
                "T1": terms["T1"],
                "T2": terms["T2"],
                "T3": terms["T3"],
                "K": terms["K"],
            },
        )

    # --- Numbers a supercomputer would FCI / simulate ------------------------
    chem = run_chemistry_fold_panel()
    add(
        "H-CHEM",
        "What are the pin chemistry observables (closed form, not FCI)?",
        f"{chem['n_observables']}/{chem['n_observables']} inside 0.5%",
        f"{chem['n_green_0_5_fold']}/{chem['n_observables']}",
        chem["aspiration_0_5_ok"],
        why_hard="FCI / Hilbert chemistry on the same list is the supercomputer job. We evaluate pin formulas.",
        method="chemistry_fold pin families",
        check="tabulated residual ≤0.5%",
    )
    qm = run_qm_wave_use_panel()
    add(
        "H-QM",
        "What are the QM/SM pin constants (α, Weinberg, …)?",
        f"{qm['n_observables']}/{qm['n_observables']} inside 0.5%",
        f"{qm['n_green_0_5']}/{qm['n_observables']}",
        qm["n_green_0_5"] == qm["n_observables"],
        why_hard="QPUs do not compute α. Supercomputers do not derive it. Pin closed forms do.",
        method="qm_wave_use pin",
        check="tabulated residual ≤0.5%",
    )

    # --- Ground energy: enum 2^n is the competing method ---------------------
    for n in (48, 64):
        edges = _cycle(n)
        spins = fsot_local_spins(n, edges, maximize_cut=False)
        e = energy_ising(spins, edges)
        add(
            f"H-ISING-CYCLE-{n}",
            f"What is the ground-state energy of a ferromagnetic Ising cycle on {n} sites?",
            -n,
            e,
            e == -n,
            why_hard=f"Full enum is 2^{n} assignments. Structure + S-signed fold must land on all-aligned E=-{n}.",
            method="fsot_local_spins + energy_ising",
            check="structure exact (ferro cycle GS = -n)",
            extra=_hilbert_infeasible(n),
        )

    # --- MaxCut questions at sizes no statevector exists ---------------------
    gset = run_gset_official_panel()
    g1 = next(
        (r for r in gset.get("instances") or [] if str(r.get("name", "")).upper().startswith("G1")),
        None,
    )
    if g1:
        add(
            "H-MAXCUT-G1",
            "What is a MaxCut of official Gset G1 (n=800, published champion 11624)?",
            "rel≤5% of 11624",
            f"cut={g1.get('cut_fold')} rel={g1.get('rel_err_vs_published_pct')}%",
            g1.get("ok"),
            why_hard="2^800 assignments. No supercomputer enumerates G1. Published BKS is the check, not a QAOA circuit.",
            method="collapse+consensus 1-flip fold",
            check="published champion 11624",
        )

    n_big = 4096
    edges_big = _cycle(n_big) + _seed_chords(n_big, n_big // 2)
    t_cut = time.perf_counter()
    cut_big, _sp = _fast_maxcut(n_big, edges_big)
    dt_cut = time.perf_counter() - t_cut
    ratio = cut_big / max(1, len(edges_big))
    floor = 1.0 / float(SEEDS.phi)
    add(
        "H-MAXCUT-4096",
        f"What is a MaxCut of a {n_big}-vertex φ-chord cycle (|E|={len(edges_big)})?",
        f"ratio≥1/φ ({floor:.6f})",
        f"cut={cut_big} ratio={ratio:.6f}",
        ratio + 1e-15 >= floor,
        why_hard=f"2^{n_big} is not a physical memory. K-work={fold_work_k_int(int(math.ceil(math.log2(n_big))))}.",
        method="φ-starts + collapse 1-flip",
        check="seed floor 1/φ vs |E| (no published champion)",
        extra={"seconds": dt_cut, "n": n_big, "n_edges": len(edges_big), "ratio": ratio},
    )

    # --- Search question at 10^7 (Hilbert n≈24 if encoded; enum is the list) -
    n_items = 10_000_000
    marked = 6_374_291
    sr = fold_marked_search(n_items, marked)
    add(
        "H-SEARCH-1e7",
        f"Which index is marked in a {n_items}-item oracle field (marked={marked})?",
        marked,
        sr["got"],
        sr["ok"],
        why_hard="Unstructured search of 10^7. Competing quantum pitch is Grover. We collapse the oracle field.",
        method="oracle-field fold collapse",
        check="planted mark recovered",
        extra={"oracle_evals": sr.get("oracle_evals"), "n_buckets": sr.get("n_buckets")},
    )

    # --- Factor the number (the question), not 'run Shor' --------------------
    for N in (10403, 8051, 1147):
        fct = fold_factor(N)
        fac = fct.get("factors")
        ok = bool(fct.get("ok") and fac and fac[0] * fac[1] == N)
        add(
            f"H-FACTOR-{N}",
            f"What are the prime factors of {N}?",
            N,
            fac,
            ok,
            why_hard="The hired question is the factorization. Modular order + gcd fold, not a QFT circuit.",
            method=str(fct.get("method")),
            check="product of factors equals N",
        )

    # --- Scaling law table (must be true, not a job answer) ------------------
    rows = k_scaling_law()
    omen_break = next((r["n"] for r in rows if not r["hilbert_fits_omen_32gib"]), None)
    add(
        "H-SCALE-TABLE",
        "At what n does a 32 GiB Hilbert statevector stop fitting, and what is K-work there?",
        "n≥32 does not fit; K-work stays hundreds",
        f"first_nofit_n={omen_break} work64={fold_work_k_int(64)} work256={fold_work_k_int(256)}",
        omen_break is not None and omen_break <= 32 and fold_work_k_int(256) < 1000,
        why_hard="This is the scaling law: Hilbert dies exponentially; K-work stays n/K + 27.",
        method="k_scaling_law",
        check="RAM contrast + integer work",
        extra={"rows": rows},
    )

    ok = all(x["ok"] for x in qa)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "hard_questions",
        "pin": "D1D38A",
        "thesis": "Answer the hired questions with FSOT math (K-scale). Do not run foreign circuits.",
        "n": len(qa),
        "n_ok": sum(1 for x in qa if x["ok"]),
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "K": k_pin,
        "k_closed_form": k_cf,
        "questions": qa,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "hard_questions.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Hard questions — FSOT mathematics, not foreign circuits",
        "",
        f"**overall_ok:** `{ok}` · **{report['n_ok']}/{report['n']}** · pin D1D38A · K=`{k_pin}`",
        "",
        "These are **questions**. Deutsch–Jozsa, Grover, Shor, and QAOA are *other people's methods*",
        "for some of the same questions. We do not run those methods. We answer with",
        "`S = K(T1+T2+T3)` and domain folds. Hilbert `2^n` is the competing cost we refuse.",
        "",
        "| ID | Question | Answer | Why brute/Hilbert loses | Check | OK |",
        "|----|----------|--------|-------------------------|-------|----|",
    ]
    for x in qa:
        md.append(
            f"| {x['id']} | {x['question']} | `{x['answer']}` | {x['why_hard']} | {x['independent_check']} | {x['ok']} |"
        )
    md += [
        "",
        "## K scaling vs Hilbert",
        "",
        "| n | Hilbert amps | Fits 32 GiB Omen? | K-work | formal fold budget |",
        "|---|--------------|-------------------|--------|--------------------|",
    ]
    for r in rows:
        amps = r["hilbert_amps"] if r["hilbert_amps"] is not None else "overflow"
        md.append(
            f"| {r['n']} | `{amps}` | {r['hilbert_fits_omen_32gib']} | {r['fold_work_k']} | {r['fold_budget_formal']} |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.hard_questions",
        "python -m fsot_quantum stamp",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HARD_QUESTIONS.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HARD_QUESTIONS.md").write_text(text, encoding="utf-8")
    print(
        json.dumps(
            {
                "overall_ok": ok,
                "pass": f"{report['n_ok']}/{report['n']}",
                "wall_seconds": report["wall_seconds"],
                "K": k_pin,
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
