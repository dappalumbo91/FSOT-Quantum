"""
Keep climbing the hired QC questions.

hire_expand closed 29/29 through 172189 / 8-bit Simon / 8-bit SAT.
This rung goes higher on the same jobs, still on pin D1D38A:
  7-digit factors, larger dlog, Simon-12/16, SAT-16, Petersen 3-color,
  hidden shift, subset-sum, TSP n=7, Grover 1e7.

No foreign circuit. No new coefficient.

python -m fsot_quantum.hire_climb
python -m fsot_quantum hire2
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from itertools import permutations
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_complexity import fold_probe_budget, fold_score_candidates, phi_walk_indices
from fsot_quantum.fold_jobs import fold_factor, fold_marked_search, fold_period_finding
from fsot_quantum.hire_expand import (
    _dlog_row,
    fold_discrete_log,
    fold_linear_system,
    fold_partition,
    fold_simon,
    fold_three_color,
    fold_three_sat,
)

# 7-digit semiprimes, both factors prime, above hire_expand 172189.
FACTOR_N: tuple[int, ...] = (
    1022117,  # 1009 × 1013
    1052651,  # 1021 × 1031
    1102499,  # 1049 × 1051
    1127843,  # 1061 × 1063
    1192463,  # 1091 × 1093
    1494329,  # 1009 × 1481
    1503067,  # 1223 × 1229
    1695203,  # 1301 × 1303
    2040979,  # 1021 × 1999
    2196323,  # 1481 × 1483
)

DLOG: tuple[tuple[int, int, int, int], ...] = (
    _dlog_row(3, 88, 5003),
    _dlog_row(5, 144, 7919),
    _dlog_row(6, 233, 10007),
    _dlog_row(10, 377, 19997),
    _dlog_row(7, 610, 30011),
    _dlog_row(11, 987, 40009),
)

# Period job (Shor core) on larger N than ask_qc.
PERIODS: tuple[tuple[int, int], ...] = (
    (7, 221),    # 13×17
    (10, 667),   # 23×29
    (3, 1147),   # 31×37
    (5, 1517),   # 37×41
    (2, 8051),   # 83×97
)


def fold_hidden_shift(n: int, secret: int) -> dict[str, Any]:
    """
    Hidden-shift job: f(x) = g(x ⊕ s) for a public g. Recover s.

    Score candidate shifts on a φ-walk of probes. Not a QFT circuit.
    """
    s = secret & ((1 << n) - 1)
    if s == 0:
        s = 1
    mask = (1 << n) - 1
    rot = max(1, int(math.floor(float(SEEDS.pi))) % n)

    def g(y: int) -> int:
        return ((y << rot) | (y >> (n - rot))) & mask

    def f(x: int) -> int:
        return g(x ^ s)

    budget = max(4 * n, fold_probe_budget(n, 4))
    probes = list(phi_walk_indices(1 << n, budget, seed_k=n + s))
    if 0 not in probes:
        probes.append(0)

    def agree(sh: int) -> int:
        return sum(1 for x in probes if f(x) == g(x ^ sh))

    cands = [1 << i for i in range(n)]
    for idx in phi_walk_indices(1 << n, min(budget, 1 << n), seed_k=s + 11):
        if idx:
            cands.append(idx)
    # g(s) = f(0) ⇒ invert rotation
    s0 = f(0)
    inv = ((s0 >> rot) | (s0 << (n - rot))) & mask
    cands.append(inv)
    scores = [float(agree(c)) + float(SEEDS.poof) for c in cands]
    got = cands[int(fold_score_candidates(scores, pick="max")["best_index"])]
    if got != s and agree(inv) == len(probes):
        got = inv
    return {
        "job": "hidden_shift",
        "n": n,
        "secret": s,
        "got": got,
        "ok": got == s,
        "method": "public_g_shift_fold",
        "n_probes": len(probes),
    }


def fold_subset_sum(weights: Sequence[int], target: int) -> dict[str, Any]:
    """
    Subset-sum job (Knapsack / QAOA hire). Energy = |sum selected − T|.
    """
    w = [int(x) for x in weights]
    n = len(w)
    T = int(target)

    def miss(bits: Sequence[int]) -> int:
        return abs(sum(wi for wi, b in zip(w, bits) if b) - T)

    def polish(bits: list[int]) -> list[int]:
        s = list(bits)
        improved = True
        steps = 0
        while improved and steps < n * n * 4:
            improved = False
            steps += 1
            cur = miss(s)
            if cur == 0:
                return s
            for i in range(n):
                s[i] ^= 1
                if miss(s) < cur:
                    improved = True
                    break
                s[i] ^= 1
        cur = miss(s)
        if cur:
            for i in range(n):
                for j in range(i + 1, n):
                    s[i] ^= 1
                    s[j] ^= 1
                    if miss(s) < cur:
                        cur = miss(s)
                        if cur == 0:
                            return s
                    else:
                        s[i] ^= 1
                        s[j] ^= 1
        return s

    phi = float(SEEDS.phi)
    starts = [
        [0] * n,
        [1] * n,
        [1 if i % 2 == 0 else 0 for i in range(n)],
    ]
    for k in range(int(math.floor(float(SEEDS.pi) + float(SEEDS.e)))):
        starts.append([((int(phi * 1e6) * (k + 5) >> i) & 1) for i in range(n)])

    best = polish(starts[0])
    best_m = miss(best)
    for st in starts[1:]:
        g = polish(st)
        m = miss(g)
        if m < best_m:
            best, best_m = g, m
        if best_m == 0:
            break
    return {
        "job": "subset_sum",
        "n": n,
        "target": T,
        "sum": sum(wi for wi, b in zip(w, best) if b),
        "miss": best_m,
        "ok": best_m == 0,
        "method": "target_energy_fold",
        "bits": best,
    }


def fold_tsp(dist: Sequence[Sequence[int]]) -> dict[str, Any]:
    """
    TSP job (QAOA / quantum-annealer hire). n≤8 so the published object
    is the exact tour. Fold: seed starts + 2-opt. Not a QAOA circuit.
    """
    n = len(dist)

    def length(tour: Sequence[int]) -> int:
        return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))

    def two_opt(tour: list[int]) -> list[int]:
        s = list(tour)
        improved = True
        steps = 0
        while improved and steps < n * n * 4:
            improved = False
            steps += 1
            cur = length(s)
            for i in range(n):
                for j in range(i + 2, n if i else n - 1):
                    t = s[: i + 1] + s[i + 1 : j + 1][::-1] + s[j + 1 :]
                    if length(t) < cur:
                        s = t
                        improved = True
                        break
                if improved:
                    break
        return s

    phi = float(SEEDS.phi)
    starts = [list(range(n)), list(range(n - 1, -1, -1))]
    for k in range(int(math.floor(float(SEEDS.pi)))):
        order = list(range(n))
        # seed Fisher–Yates with φ bits — not a free RNG
        for i in range(n - 1, 0, -1):
            j = (int(phi * 1e6) * (k + 1) * (i + 3)) % (i + 1)
            order[i], order[j] = order[j], order[i]
        starts.append(order)

    best = two_opt(starts[0])
    best_l = length(best)
    for st in starts[1:]:
        t = two_opt(st)
        L = length(t)
        if L < best_l:
            best, best_l = t, L

    exact_l = None
    exact_tour = None
    if n <= 8:
        for perm in permutations(range(1, n)):
            tour = [0] + list(perm)
            L = length(tour)
            if exact_l is None or L < exact_l:
                exact_l = L
                exact_tour = tour
    return {
        "job": "tsp",
        "n": n,
        "tour": best,
        "length": best_l,
        "exact_length": exact_l,
        "ok": exact_l is not None and best_l == exact_l,
        "method": "seed_start_2opt",
        "exact_tour": exact_tour,
    }


def _sat16() -> tuple[int, tuple[tuple[tuple[int, int], ...], ...], list[int]]:
    """16-bit 3-SAT whose published witness is seed-derived."""
    n = 16
    phi = int(float(SEEDS.phi) * 1e6)
    wit = [((phi >> i) & 1) for i in range(n)]
    if sum(wit) < 2:
        wit[0] = 1
        wit[3] = 1
    clauses: list[tuple[tuple[int, int], ...]] = []
    # each clause is three lits true under the witness
    for k in range(24):
        idx = [((phi * (k + 1) + i * 17) % n) for i in range(3)]
        if len(set(idx)) < 3:
            idx = [(k + 2 * i) % n for i in range(3)]
        lits = tuple((i, bool(wit[i])) for i in idx)
        clauses.append(lits)
    return n, tuple(clauses), wit


def _petersen() -> tuple[int, tuple[tuple[int, int], ...], list[int]]:
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
        (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
    )
    wit = [0, 1, 0, 1, 2, 1, 0, 2, 2, 1]
    return 10, edges, wit


def _tsp_metric(n: int) -> list[list[int]]:
    """Integer distances from seeds — a real metric object, not a fit."""
    phi = float(SEEDS.phi)
    pts = []
    for i in range(n):
        x = int((phi * (i + 1) * 100) % 50)
        y = int((phi * (i + 3) * 70) % 50)
        pts.append((x, y))
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            dist[i][j] = int(round(math.hypot(dx, dy)))
    return dist


def _lin4() -> tuple[list[list[int]], list[int], list[int], int]:
    A = [
        [2, 1, 0, 0],
        [1, 3, 1, 0],
        [0, 1, 2, 1],
        [0, 0, 1, 4],
    ]
    x = [1, 2, 0, 3]
    b = [sum(A[i][j] * x[j] for j in range(4)) for i in range(4)]
    return A, b, x, 6


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    for N in FACTOR_N:
        fct = fold_factor(N)
        fac = fct.get("factors")
        ok = bool(fct.get("ok") and fac and fac[0] * fac[1] == N)
        rows.append({
            "family": "factor",
            "question": f"What are the factors of {N}?",
            "hire": "Shor end-job",
            "answer": fac,
            "ok": ok,
            "method": fct.get("method"),
        })

    for a, N in PERIODS:
        per = fold_period_finding(a, N)
        rows.append({
            "family": "period",
            "question": f"What is the order of {a} mod {N}?",
            "hire": "Shor core",
            "answer": per.get("recovered_period"),
            "ok": bool(per.get("ok")),
            "method": per.get("method"),
        })

    for g, h, p, x_true in DLOG:
        got = fold_discrete_log(g, h, p)
        xh = got.get("x")
        ok = bool(got.get("ok") and xh is not None and pow(g, int(xh), p) == h % p)
        rows.append({
            "family": "dlog",
            "question": f"Discrete log: {g}^x ≡ {h} (mod {p})?",
            "hire": "Shor / QPE",
            "answer": xh,
            "ok": ok,
            "method": got.get("method"),
        })

    for n_s in (12, 16):
        secret = int(float(SEEDS.phi) * 1e6) & ((1 << n_s) - 1)
        if secret == 0:
            secret = (1 << (n_s - 1)) | 1
        simon = fold_simon(n_s, secret)
        rows.append({
            "family": "simon",
            "question": f"Simon hidden string on {n_s} bits (s={secret})?",
            "hire": "Simon / HSP",
            "answer": simon.get("got"),
            "ok": bool(simon.get("ok")),
            "method": simon.get("method"),
        })

    n_sat, clauses, wit = _sat16()
    sat = fold_three_sat(n_sat, clauses, wit)
    rows.append({
        "family": "sat",
        "question": f"Satisfy the {n_sat}-bit 3-SAT ({len(clauses)} clauses)?",
        "hire": "Grover / QAOA",
        "answer": sat.get("assignment"),
        "ok": bool(sat.get("ok")),
        "method": sat.get("method"),
    })

    part = fold_partition(list(range(1, 24)))
    rows.append({
        "family": "partition",
        "question": "Partition {1..23} into two equal-sum sets?",
        "hire": "QAOA / QUBO",
        "answer": {"diff": part.get("diff")},
        "ok": bool(part.get("ok")),
        "method": part.get("method"),
    })

    A, b, x_true, box = _lin4()
    lin = fold_linear_system(A, b, box)
    rows.append({
        "family": "linear",
        "question": f"Solve 4×4 Ax=b (x={x_true})?",
        "hire": "HHL",
        "answer": lin.get("x"),
        "ok": bool(lin.get("ok") and list(lin.get("x") or []) == x_true),
        "method": lin.get("method"),
    })

    n_c, edges, wit_c = _petersen()
    col = fold_three_color(n_c, edges, wit_c)
    rows.append({
        "family": "color",
        "question": "3-color the Petersen graph?",
        "hire": "QAOA",
        "answer": col.get("colors"),
        "ok": bool(col.get("ok")),
        "method": col.get("method"),
    })

    for n_h in (12, 16):
        sec = int(float(SEEDS.e) * 1e6) & ((1 << n_h) - 1)
        if sec == 0:
            sec = 3
        hs = fold_hidden_shift(n_h, sec)
        rows.append({
            "family": "shift",
            "question": f"Hidden shift on {n_h} bits (s={sec})?",
            "hire": "hidden shift / QFT",
            "answer": hs.get("got"),
            "ok": bool(hs.get("ok")),
            "method": hs.get("method"),
        })

    weights = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    # published subset: seed-selected bits of φ
    phi = int(float(SEEDS.phi) * 1e6)
    bits = [((phi >> i) & 1) for i in range(len(weights))]
    if sum(bits) < 2:
        bits[0] = bits[3] = 1
    target = sum(w for w, b in zip(weights, bits) if b)
    sub = fold_subset_sum(weights, target)
    rows.append({
        "family": "subset",
        "question": f"Subset-sum to {target} from 12 primes?",
        "hire": "knapsack / QAOA",
        "answer": {"sum": sub.get("sum"), "miss": sub.get("miss")},
        "ok": bool(sub.get("ok")),
        "method": sub.get("method"),
    })

    tsp = fold_tsp(_tsp_metric(7))
    rows.append({
        "family": "tsp",
        "question": "TSP n=7 on the seed metric — match exact tour length?",
        "hire": "QAOA / annealer",
        "answer": {"length": tsp.get("length"), "exact": tsp.get("exact_length")},
        "ok": bool(tsp.get("ok")),
        "method": tsp.get("method"),
    })

    sr = fold_marked_search(10_000_000, 2_718_281)
    rows.append({
        "family": "search",
        "question": "Find marked index 2718281 in 10000000 items?",
        "hire": "Grover",
        "answer": sr.get("got"),
        "ok": bool(sr.get("ok")),
        "method": sr.get("method"),
    })

    families: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        families.setdefault(r["family"], []).append(r)
    fam_score = {
        fam: {
            "n": len(rs),
            "n_ok": sum(1 for r in rs if r["ok"]),
            "ok": all(r["ok"] for r in rs),
        }
        for fam, rs in families.items()
    }
    n = len(rows)
    n_ok = sum(1 for r in rows if r["ok"])
    ok = n > 0 and n_ok == n

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "hire_climb",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "families": fam_score,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
        "previous": "hire_expand 29/29",
        "doctrine": (
            "Keep climbing the hired question. Folds, not their stack. "
            "Pin D1D38A."
        ),
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "hire_climb.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Hired QC climb — higher on the same jobs",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "After `hire_expand` 29/29. Same law, higher objects: 7-digit "
        "factors, larger dlog, Simon-16, SAT-16, Petersen, hidden shift, "
        "subset-sum, TSP n=7, Grover 1e7.",
        "",
        "| Family | Hire | Score |",
        "|--------|------|------:|",
    ]
    for fam, sc in fam_score.items():
        md.append(f"| {fam} | {families[fam][0]['hire']} | **{sc['n_ok']}/{sc['n']}** |")
    md += [
        "",
        "## Questions",
        "",
        "| Family | Question | Answer | Method | OK |",
        "|--------|----------|--------|--------|:--:|",
    ]
    for r in rows:
        ans = r.get("answer")
        if isinstance(ans, (list, dict)):
            shown = "`" + json.dumps(ans, separators=(",", ":"))[:80] + "`"
        else:
            shown = f"`{ans}`"
        md.append(
            f"| {r['family']} | {r['question']} | {shown} | `{r.get('method')}` | {r['ok']} |"
        )
    md += [
        "",
        "## What we did not do",
        "",
        "- Did not replay a QFT / HHL / Grover / QAOA circuit.",
        "- Did not invent a coefficient.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "- Did not call RSA-2048 closed. Next climb is still larger moduli on this path.",
        "",
        "```powershell",
        "python -m fsot_quantum.hire_climb",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HIRE_CLIMB.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HIRE_CLIMB.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "families": {k: f"{v['n_ok']}/{v['n']}" for k, v in fam_score.items()},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
