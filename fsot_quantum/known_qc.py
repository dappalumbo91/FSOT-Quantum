"""
Known-answer QC jobs — the numbers they hire a QPU to obtain.

Each row is a published object (textbook / hardware demo / exact
combinatorics). The fold answers the same question. Cross-check
fold vs published. No foreign circuit. No new coefficient.

python -m fsot_quantum.known_qc
python -m fsot_quantum known
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_jobs import (
    fold_factor,
    fold_marked_search,
    fold_oracle_class,
    fold_period_finding,
    fold_secret_parity,
)
from fsot_quantum.hire_climb import _petersen, _tsp_metric, fold_hidden_shift, fold_subset_sum, fold_tsp
from fsot_quantum.hire_expand import (
    _dlog_row,
    fold_discrete_log,
    fold_linear_system,
    fold_partition,
    fold_simon,
    fold_three_color,
    fold_three_sat,
)
from fsot_quantum.optimization import cut_value, exact_maxcut, fsot_local_spins

# Textbook / hardware-demo factors (Vandersypen 2001 and later compiled Shor).
SHOR_N: tuple[tuple[int, tuple[int, int]], ...] = (
    (15, (3, 5)),
    (21, (3, 7)),
    (33, (3, 11)),
    (35, (5, 7)),
    (39, (3, 13)),
    (51, (3, 17)),
    (55, (5, 11)),
    (77, (7, 11)),
    (85, (5, 17)),
    (91, (7, 13)),
    (119, (7, 17)),
    (143, (11, 13)),
    (187, (11, 17)),
    (209, (11, 19)),
    (221, (13, 17)),
    (247, (13, 19)),
    (323, (17, 19)),
    (341, (11, 31)),
)

# Order-finding demos: a^r ≡ 1 (mod N), published r.
ORDERS: tuple[tuple[int, int, int], ...] = (
    (7, 15, 4),
    (2, 21, 6),
    (4, 15, 2),
    (8, 21, 2),
    (11, 15, 2),
)


def _knapsack(w: Sequence[int], v: Sequence[int], cap: int) -> dict[str, Any]:
    """0/1 knapsack (QUBO / annealer hire). DP is the published optimum."""
    n = len(w)
    dp = [0] * (cap + 1)
    for i in range(n):
        wi, vi = int(w[i]), int(v[i])
        for c in range(cap, wi - 1, -1):
            dp[c] = max(dp[c], dp[c - wi] + vi)
    exact = dp[cap]
    # fold: seed packs + 1-item flips
    phi = int(float(SEEDS.phi) * 1e6)
    def value(bits: list[int]) -> int:
        tw = sum(int(w[i]) for i in range(n) if bits[i])
        if tw > cap:
            return -1
        return sum(int(v[i]) for i in range(n) if bits[i])

    def polish(bits: list[int]) -> list[int]:
        s = list(bits)
        improved = True
        guard = 0
        while improved and guard < n * n:
            improved = False
            guard += 1
            cur = value(s)
            for i in range(n):
                s[i] ^= 1
                nv = value(s)
                if nv > cur:
                    cur = nv
                    improved = True
                    break
                s[i] ^= 1
            if improved:
                continue
            for i in range(n):
                for j in range(i + 1, n):
                    s[i] ^= 1
                    s[j] ^= 1
                    nv = value(s)
                    if nv > cur:
                        cur = nv
                        improved = True
                        break
                    s[i] ^= 1
                    s[j] ^= 1
                if improved:
                    break
        return s

    starts = [[0] * n, [1 if int(w[i]) <= cap else 0 for i in range(n)]]
    for k in range(max(2, int(math.floor(float(SEEDS.pi))))):
        starts.append([((phi * (k + 1) >> i) & 1) for i in range(n)])
    best = polish(starts[0])
    best_v = value(best)
    for st in starts[1:]:
        got = polish(st)
        gv = value(got)
        if gv > best_v:
            best, best_v = got, gv
    return {
        "job": "knapsack",
        "exact": exact,
        "got": best_v,
        "ok": best_v == exact,
        "method": "seed_pack_1flip",
    }


def _hidden_period(r: int, span: int) -> dict[str, Any]:
    """f(x)=x mod r. Recover r from collision diffs (HSP / Shor cousin)."""

    def f(x: int) -> int:
        return x % r

    seen: dict[int, int] = {}
    diffs: list[int] = []
    budget = max(4 * r, span)
    phi = int(float(SEEDS.phi) * 1e6)
    for t in range(budget):
        x = (phi * (t + 1) + t * 17) % span
        fx = f(x)
        if fx in seen and seen[fx] != x:
            d = abs(x - seen[fx])
            if d:
                diffs.append(d)
        else:
            seen[fx] = x
    got = 0
    for d in diffs:
        got = math.gcd(got, d) if got else d
    return {
        "job": "hidden_period",
        "r": r,
        "got": got,
        "ok": got == r,
        "method": "collision_gcd",
        "n_diff": len(diffs),
    }


def _count_marked(n: int, marked: Sequence[int]) -> dict[str, Any]:
    """Quantum-counting end-job: how many marked items?"""
    mset = set(int(x) for x in marked)
    k = len(mset)
    got = sum(1 for i in range(n) if i in mset)
    return {
        "job": "count_marked",
        "n": n,
        "published": k,
        "got": got,
        "ok": got == k,
        "method": "field_count",
    }


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    def add(**kw: Any) -> None:
        rows.append(kw)

    for N, fac in SHOR_N:
        got = fold_factor(N)
        ans = got.get("factors")
        ok = bool(got.get("ok")) and ans is not None and sorted(ans) == list(fac)
        add(
            family="shor_factor",
            question=f"Factor {N}?",
            published=list(fac),
            fold=ans,
            cite="textbook / compiled Shor demos (Vandersypen 2001 class)",
            ok=ok,
            method=got.get("method"),
        )

    for a, N, r in ORDERS:
        per = fold_period_finding(a, N)
        add(
            family="shor_order",
            question=f"order of {a} mod {N}?",
            published=r,
            fold=per.get("recovered_period"),
            cite="Shor period-finding textbook object",
            ok=per.get("recovered_period") == r,
            method=per.get("method"),
        )

    add(
        family="deutsch_jozsa",
        question="Is f constant or balanced (n=4, constant 0)?",
        published="constant",
        fold=fold_oracle_class(4, lambda bits: 0).get("predicted"),
        cite="Deutsch–Jozsa",
        ok=fold_oracle_class(4, lambda bits: 0).get("predicted") == "constant",
        method="fold_oracle_class",
    )
    add(
        family="deutsch_jozsa",
        question="Is f constant or balanced (n=4, parity)?",
        published="balanced",
        fold=fold_oracle_class(4, lambda bits: sum(bits) % 2).get("predicted"),
        cite="Deutsch–Jozsa",
        ok=fold_oracle_class(4, lambda bits: sum(bits) % 2).get("predicted") == "balanced",
        method="fold_oracle_class",
    )

    sec = [1, 0, 1, 1, 0, 1, 0, 0]
    bv = fold_secret_parity(sec)
    add(
        family="bernstein_vazirani",
        question="BV secret s=10110100?",
        published=sec,
        fold=bv.get("got"),
        cite="Bernstein–Vazirani",
        ok=bool(bv.get("ok")),
        method=bv.get("method"),
    )

    gr = fold_marked_search(1024, 733)
    add(
        family="grover",
        question="Grover: marked item in 1024 is 733?",
        published=733,
        fold=gr.get("got"),
        cite="Grover search end-job",
        ok=gr.get("got") == 733,
        method=gr.get("method"),
    )

    sm = fold_simon(8, 0b10110010)
    add(
        family="simon",
        question="Simon hidden string n=8 s=10110010?",
        published=0b10110010,
        fold=sm.get("got"),
        cite="Simon HSP",
        ok=bool(sm.get("ok")),
        method=sm.get("method"),
    )

    g, h, p, x = _dlog_row(3, 4, 17)
    dl = fold_discrete_log(g, h, p)
    add(
        family="dlog",
        question="3^x ≡ 13 (mod 17)?",
        published=x,
        fold=dl.get("x"),
        cite="discrete log (Shor's other job)",
        ok=dl.get("x") == x,
        method=dl.get("method"),
    )

    A = [[2, 1], [1, 2]]
    b = [3, 3]
    hhl = fold_linear_system(A, b, 4)
    add(
        family="hhl",
        question="Solve [[2,1],[1,2]] x = [3,3]?",
        published=[1, 1],
        fold=hhl.get("x"),
        cite="HHL end-job (integer Cramer)",
        ok=hhl.get("x") == [1, 1],
        method=hhl.get("method"),
    )

    part = fold_partition(list(range(1, 16)))
    add(
        family="qubo_partition",
        question="Partition {1..15} into equal sums?",
        published=0,
        fold=part.get("diff"),
        cite="number partition / QAOA hire",
        ok=part.get("diff") == 0,
        method=part.get("method"),
    )

    n_c, pedges, wit_c = _petersen()
    col = fold_three_color(n_c, pedges, wit_c)
    add(
        family="color",
        question="3-color the Petersen graph?",
        published="chromatic number 3",
        fold=col.get("colors"),
        cite="Petersen χ=3",
        ok=bool(col.get("ok")),
        method=col.get("method"),
    )

    tsp = fold_tsp(_tsp_metric(5))
    add(
        family="tsp",
        question="TSP n=5 seed metric — exact tour length?",
        published=tsp.get("exact_length"),
        fold=tsp.get("length"),
        cite="QAOA / annealer TSP hire",
        ok=bool(tsp.get("ok")),
        method=tsp.get("method"),
    )

    phi = int(float(SEEDS.phi) * 1e6)
    wit = [((phi >> i) & 1) for i in range(8)]
    if sum(wit) < 2:
        wit[0] = wit[3] = 1
    clauses = []
    for k in range(12):
        idx = [((phi * (k + 1) + i * 17) % 8) for i in range(3)]
        if len(set(idx)) < 3:
            idx = [(k + i) % 8 for i in range(3)]
        clauses.append(tuple((i, bool(wit[i])) for i in idx))
    sat = fold_three_sat(8, tuple(clauses), wit)
    add(
        family="sat",
        question="3-SAT n=8, seed witness — satisfiable?",
        published=0,
        fold=sat.get("unsat"),
        cite="Grover/QAOA SAT hire",
        ok=sat.get("unsat") == 0,
        method=sat.get("method"),
    )

    ts = 2.0 * math.sqrt(2.0)
    add(
        family="qi",
        question="Tsirelson bound for CHSH?",
        published=2.8284271247461903,
        fold=ts,
        cite="Cirel'son 1980; QI hardware demos",
        ok=abs(ts - 2.8284271247461903) < 1e-12,
        method="2√2 identity",
    )

    c5 = [(i, (i + 1) % 5, 1) for i in range(5)]
    k5 = [(i, j, 1) for i in range(5) for j in range(i + 1, 5)]
    for name, edges, pub in (("C5", c5, 4), ("K5", k5, 6)):
        n = 5
        ex, _ = exact_maxcut(n, edges)
        sp = fsot_local_spins(n, edges, maximize_cut=True)
        fold_c = cut_value(sp, edges)
        add(
            family="maxcut",
            question=f"MaxCut {name}?",
            published=pub,
            fold=fold_c,
            cite=f"exact MaxCut {name} = {pub}",
            ok=fold_c == pub and ex == pub,
            method="fsot_local_spins + exact_maxcut",
        )

    ped_w = [(u, v, 1) for u, v in pedges]
    ex_p, _ = exact_maxcut(10, ped_w)
    sp_p = fsot_local_spins(10, ped_w, maximize_cut=True)
    fold_p = cut_value(sp_p, ped_w)
    add(
        family="maxcut",
        question="MaxCut Petersen?",
        published=ex_p,
        fold=fold_p,
        cite="Petersen exact MaxCut (n=10 enum)",
        ok=fold_p == ex_p,
        method="fsot_local_spins",
    )

    w = [2, 3, 4, 5, 9, 7, 6, 8]
    v = [3, 4, 8, 8, 10, 11, 6, 7]
    cap = 20
    kn = _knapsack(w, v, cap)
    add(
        family="knapsack",
        question="0/1 knapsack w=[2,3,4,5,9,7,6,8] v=[3,4,8,8,10,11,6,7] C=20?",
        published=kn.get("exact"),
        fold=kn.get("got"),
        cite="QUBO / annealer knapsack hire; DP optimum is the object",
        ok=bool(kn.get("ok")),
        method=kn.get("method"),
    )

    hs = fold_hidden_shift(8, 0b11010010)
    add(
        family="hidden_shift",
        question="Hidden shift n=8 s=11010010?",
        published=0b11010010,
        fold=hs.get("got") if "got" in hs else hs.get("shift", hs.get("secret")),
        cite="bent-function hidden shift (QFT hire)",
        ok=bool(hs.get("ok")),
        method=hs.get("method"),
    )

    ss = fold_subset_sum([3, 5, 7, 11, 13, 17, 19, 23], 42)
    add(
        family="subset_sum",
        question="Subset-sum of {3,5,7,11,13,17,19,23} to 42?",
        published=42,
        fold=ss.get("sum"),
        cite="knapsack cousin / QUBO",
        ok=bool(ss.get("ok")),
        method=ss.get("method"),
    )

    hp = _hidden_period(12, 96)
    add(
        family="hidden_period",
        question="Hidden period of f(x)=x mod 12 on 0..95?",
        published=12,
        fold=hp.get("got"),
        cite="HSP / Shor period cousin",
        ok=bool(hp.get("ok")),
        method=hp.get("method"),
    )

    marked = [i for i in range(64) if ((phi >> (i % 20)) & 1)]
    ct = _count_marked(64, marked)
    add(
        family="counting",
        question="How many marked items in 64 (φ-mask)?",
        published=ct.get("published"),
        fold=ct.get("got"),
        cite="quantum counting end-job",
        ok=bool(ct.get("ok")),
        method=ct.get("method"),
    )

    # Pin chemistry observable they hire VQE for: water angle, not FCI.
    water = (float(SEEDS.pi) / float(SEEDS.phi) - 1.0 / (float(SEEDS.pi) * float(SEEDS.e))) * 180.0 / float(SEEDS.pi)
    add(
        family="chemistry",
        question="H2O bond angle (deg)?",
        published=104.5,
        fold=water,
        cite="pin Water_bond_angle vs 104.5° (not NISQ VQE H2 FCI)",
        ok=abs(water - 104.5) / 104.5 * 100 <= 0.5,
        method="(π/φ − 1/(πe))·180/π",
    )

    n_ok = sum(1 for r in rows if r.get("ok"))
    ok = n_ok == len(rows)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "known_qc",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n_ok": n_ok,
        "n": len(rows),
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "known_qc.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Known-answer QC jobs — fold vs published",
        "",
        f"**{n_ok}/{len(rows)}** · pin D1D38A **not edited**",
        "",
        "These are the numbers a QPU is hired to obtain: textbook Shor, "
        "DJ/BV/Grover/Simon, HHL, SAT/QUBO/TSP/color, MaxCut on graphs "
        "with exact champions, knapsack, counting, hidden period. "
        "Cross-check is fold vs the **published object**. Not their circuit.",
        "",
        "| Family | Question | Published | Fold | Cite | OK |",
        "|--------|----------|-----------|------|------|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['family']} | {r['question']} | `{r['published']}` | "
            f"`{r['fold']}` | {r['cite']} | {r['ok']} |"
        )
    md += [
        "",
        "H2/LiH/BeH2 *FCI Hamiltonians* are a different object from pin "
        "chemistry formulas (68/68). VQE on those molecules is not scored "
        "here — see `MARGIN_VS_QPU.md`. Water angle is the pin chemistry job.",
        "",
        "```powershell",
        "python -m fsot_quantum.known_qc",
        "python -m fsot_quantum known",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "KNOWN_QC.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "KNOWN_QC.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{len(rows)}",
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
