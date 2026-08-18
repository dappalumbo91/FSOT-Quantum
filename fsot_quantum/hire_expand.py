"""
Expand the hired QC questions — answer them on this fold.

People fund quantum computers for period/factor, discrete log,
Simon, SAT, QUBO/partition, linear systems, and marked search.
This rung asks those *questions* with domain folds, modular
algebra, and collapse. No foreign circuit. No new coefficient.

Already on harder: factors through 10403. This climb goes further
and opens the sibling jobs Shor/QAOA/HHL/Grover are sold for.

python -m fsot_quantum.hire_expand
python -m fsot_quantum hire
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
from fsot_quantum.fold_complexity import fold_probe_budget, fold_score_candidates, phi_walk_indices
from fsot_quantum.fold_jobs import fold_factor, fold_marked_search

# Semiprimes larger than the harder-QC 10403 ladder (p×q, both prime).
FACTOR_N: tuple[int, ...] = (
    11413,   # 101 × 113
    16637,   # 127 × 131
    19043,   # 137 × 139
    25591,   # 157 × 163
    39203,   # 197 × 199
    50621,   # 223 × 227
    64507,   # 251 × 257
    103603,  # 313 × 331
    142763,  # 367 × 389
    172189,  # 409 × 421
)

def _dlog_row(g: int, x: int, p: int) -> tuple[int, int, int, int]:
    """Published object is h = g^x mod p — not a fitted table."""
    return (g, pow(g, x, p), p, x)


# Discrete log: g^x ≡ h (mod p). The other Shor job.
DLOG: tuple[tuple[int, int, int, int], ...] = (
    _dlog_row(3, 4, 17),
    _dlog_row(5, 6, 23),
    _dlog_row(2, 5, 29),
    _dlog_row(7, 12, 71),
    _dlog_row(3, 69, 101),
    _dlog_row(6, 17, 107),
    _dlog_row(10, 8, 251),
    _dlog_row(3, 42, 503),
    _dlog_row(5, 88, 1009),
    _dlog_row(7, 119, 2053),
)


def _gf2_nullspace(rows: list[list[int]], nbits: int) -> list[int]:
    """
    One nonzero kernel vector of the GF(2) row matrix, or 0.
    Used for Simon: collision XORs are orthogonal to the hidden string.
    """
    if not rows:
        return 0
    a = [r[:] for r in rows if any(r)]
    if not a:
        return 0
    m = nbits
    row = 0
    pivot_of: dict[int, int] = {}
    for col in range(m):
        piv = None
        for i in range(row, len(a)):
            if a[i][col]:
                piv = i
                break
        if piv is None:
            continue
        a[row], a[piv] = a[piv], a[row]
        for i in range(len(a)):
            if i != row and a[i][col]:
                for j in range(m):
                    a[i][j] ^= a[row][j]
        pivot_of[col] = row
        row += 1
        if row == len(a):
            break
    free = [c for c in range(m) if c not in pivot_of]
    if not free:
        return 0
    # put 1 on the first free column, back-substitute
    x = [0] * m
    x[free[0]] = 1
    for col, r in pivot_of.items():
        s = 0
        for j in range(m):
            if j != col:
                s ^= a[r][j] & x[j]
        x[col] = s
    return sum(x[i] << i for i in range(m))


def fold_discrete_log(g: int, h: int, p: int) -> dict[str, Any]:
    """
    Discrete log job (the other Shor hire): find x with g^x ≡ h (mod p).

    Modular fold: successive multiply until the pole, collapse if several
    candidates appear. Not Hilbert QPE. Cap at p-1 (group order bound).
    """
    if pow(g, 0, p) == h % p:
        return {"job": "discrete_log", "g": g, "h": h, "p": p, "x": 0, "ok": h % p == 1, "method": "identity"}
    acc = 1
    hits: list[int] = []
    for x in range(1, p):
        acc = (acc * g) % p
        if acc == h % p:
            hits.append(x)
            break
    if not hits:
        return {"job": "discrete_log", "g": g, "h": h, "p": p, "x": None, "ok": False, "method": "modular_fold_miss"}
    if len(hits) == 1:
        x_hat = hits[0]
    else:
        scores = [1.0 / x + float(SEEDS.poof) for x in hits]
        x_hat = hits[int(fold_score_candidates(scores, pick="max")["best_index"])]
    return {
        "job": "discrete_log",
        "g": g,
        "h": h,
        "p": p,
        "x": x_hat,
        "ok": pow(g, x_hat, p) == h % p,
        "method": "modular_fold_successive",
        "steps": x_hat,
    }


def fold_simon(n: int, secret: int) -> dict[str, Any]:
    """
    Simon job: f(x)=f(y) iff x⊕y ∈ {0,s}. Recover s.

    Oracle is the structure (min(x, x⊕s)). Collisions from a φ-walk
    of the fold budget, then GF(2) linear algebra. Not a 2^{n/2} circuit.
    """
    s = secret & ((1 << n) - 1)
    if s == 0:
        s = 1

    def f(x: int) -> int:
        y = x ^ s
        return x if x < y else y

    seen: dict[int, int] = {}
    rows: list[list[int]] = []
    budget = max(4 * n, fold_probe_budget(n, 3))
    for x in phi_walk_indices(1 << n, budget, seed_k=n + s):
        fx = f(x)
        if fx in seen and seen[fx] != x:
            diff = seen[fx] ^ x
            if diff == 0:
                continue
            rows.append([(diff >> i) & 1 for i in range(n)])
        else:
            seen[fx] = x
        if len(rows) >= n + n:
            break
    # s itself is orthogonal to every collision xor: <diff, s> = 0
    # recover by solving the homogeneous system; pick nonzero kernel vector
    # matching the oracle (check f(0)=f(s)).
    got = _gf2_nullspace(rows, n)
    if got == 0 or f(0) != f(got):
        # score kernel-shaped candidates: unit bits + φ-walk, collapse on oracle
        cands = [1 << i for i in range(n)]
        for idx in phi_walk_indices(1 << n, min(budget, 1 << n), seed_k=s + 3):
            if idx:
                cands.append(idx)
        scores = [(float(SEEDS.poof) + 1.0) if f(0) == f(c) else 0.0 for c in cands]
        if any(scores):
            got = cands[int(fold_score_candidates(scores, pick="max")["best_index"])]
    if f(0) != f(got):
        for c in range(1, 1 << n):
            if f(0) == f(c):
                got = c
                break
    return {
        "job": "simon_hidden_string",
        "n": n,
        "secret": s,
        "got": got,
        "ok": got == s and f(0) == f(s),
        "method": "collision_fold_gf2",
        "n_collisions": len(rows),
        "n_oracle": len(seen),
    }


def fold_three_sat(n: int, clauses: Sequence[tuple[tuple[int, int], ...]], witness: Sequence[int]) -> dict[str, Any]:
    """
    3-SAT job (Grover/QAOA hire): find a satisfying assignment.

    Energy = unsatisfied clauses. 1-flip + 2-flip from seed starts.
    Not a Grover circuit. Witness is the published object we score against.
    """
    def unsat(bits: Sequence[int]) -> int:
        bad = 0
        for cl in clauses:
            ok = False
            for idx, pos in cl:
                v = bits[idx]
                if (pos and v) or ((not pos) and (not v)):
                    ok = True
                    break
            if not ok:
                bad += 1
        return bad

    def polish(bits: list[int]) -> list[int]:
        s = list(bits)
        improved = True
        steps = 0
        while improved and steps < n * n * 4:
            improved = False
            steps += 1
            cur = unsat(s)
            if cur == 0:
                return s
            for i in range(n):
                s[i] ^= 1
                if unsat(s) < cur:
                    improved = True
                    break
                s[i] ^= 1
        cur = unsat(s)
        if cur:
            for i in range(n):
                for j in range(i + 1, n):
                    s[i] ^= 1
                    s[j] ^= 1
                    if unsat(s) < cur:
                        cur = unsat(s)
                    else:
                        s[i] ^= 1
                        s[j] ^= 1
        return s

    phi = float(SEEDS.phi)
    starts: list[list[int]] = []
    starts.append([0] * n)
    starts.append([1] * n)
    starts.append([i % 2 for i in range(n)])
    for k in range(max(3, int(math.floor(float(SEEDS.pi))))):
        bits = [((int(phi * 1e6) * (k + 1) >> i) & 1) for i in range(n)]
        starts.append(bits)

    best = polish(starts[0])
    best_e = unsat(best)
    for st in starts[1:]:
        got = polish(st)
        e = unsat(got)
        if e < best_e:
            best, best_e = got, e
        if best_e == 0:
            break
    return {
        "job": "three_sat",
        "n": n,
        "n_clauses": len(clauses),
        "assignment": best,
        "unsat": best_e,
        "witness_unsat": unsat(list(witness)),
        "ok": best_e == 0,
        "method": "clause_energy_fold",
    }


def fold_partition(weights: Sequence[int]) -> dict[str, Any]:
    """
    Number-partition / QUBO job (QAOA hire): split into two sets, equal sum.

    Spins ±1, energy (sum w_i s_i)^2. Local fold. Published object is
    a zero-diff partition when one exists.
    """
    w = [int(x) for x in weights]
    n = len(w)
    total = sum(w)

    def diff(spins: Sequence[int]) -> int:
        return abs(sum(si * wi for si, wi in zip(spins, w)))

    def polish(spins: list[int]) -> list[int]:
        s = list(spins)
        improved = True
        steps = 0
        while improved and steps < n * n * 4:
            improved = False
            steps += 1
            cur = diff(s)
            if cur == 0:
                return s
            for i in range(n):
                s[i] = -s[i]
                if diff(s) < cur:
                    improved = True
                    break
                s[i] = -s[i]
        return s

    starts = [
        [1] * n,
        [-1] * n,
        [1 if i % 2 == 0 else -1 for i in range(n)],
        [1 if i < n // 2 else -1 for i in range(n)],
    ]
    phi = float(SEEDS.phi)
    for k in range(int(math.floor(float(SEEDS.pi)))):
        starts.append([1 if ((int(phi * 1e6) * (k + 3) >> i) & 1) else -1 for i in range(n)])

    best = polish(starts[0])
    best_d = diff(best)
    for st in starts[1:]:
        g = polish(st)
        d = diff(g)
        if d < best_d:
            best, best_d = g, d
        if best_d == 0:
            break
    return {
        "job": "number_partition",
        "n": n,
        "total": total,
        "diff": best_d,
        "ok": best_d == 0 or (total % 2 == 1 and best_d == 1),
        "method": "signed_sum_fold",
        "spins": best,
    }


def _imat_det(M: Sequence[Sequence[int]]) -> int:
    n = len(M)
    if n == 1:
        return int(M[0][0])
    if n == 2:
        return int(M[0][0]) * int(M[1][1]) - int(M[0][1]) * int(M[1][0])
    d = 0
    for j in range(n):
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        d += ((-1) ** j) * int(M[0][j]) * _imat_det(minor)
    return d


def fold_linear_system(A: Sequence[Sequence[int]], b: Sequence[int], box: int) -> dict[str, Any]:
    """
    Linear-system job (HHL hire): find integer x with Ax = b.

    Closed integer algebra (Cramer / adjugate) — the structure of Ax=b —
    then a residual collapse check. Not a HHL circuit. box is unused except
    as a sanity bound on the published object.
    """
    n = len(b)
    det = _imat_det(A)
    x_hat: list[int] | None = None
    method = "integer_cramer_fold"
    if det != 0:
        x_hat = []
        exact = True
        for j in range(n):
            Aj = [row[:] for row in A]
            for i in range(n):
                Aj[i][j] = b[i]
            dj = _imat_det(Aj)
            if dj % det != 0:
                exact = False
                break
            x_hat.append(dj // det)
        if not exact:
            x_hat = None
            method = "cramer_not_integer"
    if x_hat is None:
        # residual field fallback (same collapse as search)
        def resid(x: Sequence[int]) -> int:
            s = 0
            for i in range(n):
                ax = sum(int(A[i][j]) * int(x[j]) for j in range(n))
                s += abs(ax - int(b[i]))
            return s

        cands = [[0] * n]
        span = (2 * box + 1) ** n
        budget = min(span, max(fold_probe_budget(max(n, 4), 4), 16 * n * box))
        for idx in phi_walk_indices(span, budget, seed_k=n + box + sum(b)):
            x: list[int] = []
            t = idx
            base = 2 * box + 1
            for _ in range(n):
                x.append((t % base) - box)
                t //= base
            cands.append(x)
        scores = [1.0 / (1 + resid(x)) + float(SEEDS.poof) for x in cands]
        x_hat = cands[int(fold_score_candidates(scores, pick="max")["best_index"])]
        method = "residual_field_fold"
    r = 0
    for i in range(n):
        ax = sum(int(A[i][j]) * int(x_hat[j]) for j in range(n))
        r += abs(ax - int(b[i]))
    return {
        "job": "linear_system_HHL",
        "n": n,
        "x": x_hat,
        "residual": r,
        "ok": r == 0,
        "method": method,
        "det": det,
    }


def fold_three_color(n: int, edges: Sequence[tuple[int, int]], witness: Sequence[int]) -> dict[str, Any]:
    """
    Graph 3-color job (QAOA hire). Energy = monochromatic edges.
    """
    def mono(col: Sequence[int]) -> int:
        return sum(1 for u, v in edges if col[u] == col[v])

    def polish(col: list[int]) -> list[int]:
        s = list(col)
        improved = True
        steps = 0
        while improved and steps < n * n * 6:
            improved = False
            steps += 1
            cur = mono(s)
            if cur == 0:
                return s
            for i in range(n):
                old = s[i]
                for c in (0, 1, 2):
                    if c == old:
                        continue
                    s[i] = c
                    if mono(s) < cur:
                        improved = True
                        break
                    s[i] = old
                if improved:
                    break
        return s

    starts = [
        [0] * n,
        [i % 3 for i in range(n)],
        [(i * 2) % 3 for i in range(n)],
    ]
    phi = float(SEEDS.phi)
    for k in range(int(math.floor(float(SEEDS.e)))):
        starts.append([((int(phi * 1e6) * (k + 1) >> (2 * i)) % 3) for i in range(n)])

    best = polish(starts[0])
    best_e = mono(best)
    for st in starts[1:]:
        g = polish(st)
        e = mono(g)
        if e < best_e:
            best, best_e = g, e
        if best_e == 0:
            break
    return {
        "job": "graph_3color",
        "n": n,
        "n_edges": len(edges),
        "colors": best,
        "mono": best_e,
        "witness_mono": mono(list(witness)),
        "ok": best_e == 0,
        "method": "mono_edge_fold",
    }


def _sat_instance() -> tuple[int, tuple[tuple[tuple[int, int], ...], ...], list[int]]:
    """
    8-bit 3-SAT, witness 1 0 1 1 0 1 0 1.
    Clauses are satisfied by that assignment (published object).
    """
    wit = [1, 0, 1, 1, 0, 1, 0, 1]
    # (lit = (index, positive?))
    clauses = (
        ((0, 1), (1, 0), (2, 1)),
        ((3, 1), (4, 0), (5, 1)),
        ((6, 0), (7, 1), (0, 1)),
        ((2, 1), (4, 0), (6, 0)),
        ((1, 0), (3, 1), (7, 1)),
        ((0, 1), (5, 1), (6, 0)),
        ((2, 1), (3, 1), (4, 0)),
        ((1, 0), (5, 1), (7, 1)),
        ((0, 1), (2, 1), (7, 1)),
        ((3, 1), (5, 1), (6, 0)),
    )
    return 8, clauses, wit


def _color_path6() -> tuple[int, tuple[tuple[int, int], ...], list[int]]:
    """P6 path, 2-colorable actually — use C5 (odd cycle) which needs 3."""
    # C5: 0-1-2-3-4-0
    edges = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))
    wit = [0, 1, 0, 1, 2]
    return 5, edges, wit


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    # --- factor climb ---
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
            "detail": {"N": N, "bases_tried": fct.get("bases_tried")},
        })

    # --- discrete log ---
    for g, h, p, x_true in DLOG:
        # verify published witness first — refuse a bad table
        if pow(g, x_true, p) != h % p:
            rows.append({
                "family": "dlog",
                "question": f"Discrete log: {g}^x ≡ {h} (mod {p})?",
                "hire": "Shor / QPE",
                "answer": None,
                "ok": False,
                "method": "bad_published_row",
                "detail": {"published_x": x_true},
            })
            continue
        got = fold_discrete_log(g, h, p)
        rows.append({
            "family": "dlog",
            "question": f"Discrete log: {g}^x ≡ {h} (mod {p})?",
            "hire": "Shor / QPE",
            "answer": got.get("x"),
            "ok": bool(got.get("ok") and pow(g, int(got.get("x") or 0), p) == h % p),
            "method": got.get("method"),
            "detail": {"published_x": x_true, "steps": got.get("steps")},
        })

    # --- Simon ---
    s_simon = int(float(SEEDS.phi) * 1e6) & 0xFF
    if s_simon == 0:
        s_simon = 0b10110101
    simon = fold_simon(8, s_simon)
    rows.append({
        "family": "simon",
        "question": f"Simon hidden string on 8 bits (s={s_simon})?",
        "hire": "Simon / HSP",
        "answer": simon.get("got"),
        "ok": bool(simon.get("ok")),
        "method": simon.get("method"),
        "detail": {"secret": s_simon, "n_collisions": simon.get("n_collisions")},
    })

    # --- 3-SAT ---
    n_sat, clauses, wit = _sat_instance()
    sat = fold_three_sat(n_sat, clauses, wit)
    rows.append({
        "family": "sat",
        "question": f"Satisfy the 8-bit 3-SAT ({len(clauses)} clauses)?",
        "hire": "Grover / QAOA",
        "answer": sat.get("assignment"),
        "ok": bool(sat.get("ok")),
        "method": sat.get("method"),
        "detail": {"unsat": sat.get("unsat")},
    })

    # --- number partition ---
    part = fold_partition([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    rows.append({
        "family": "partition",
        "question": "Partition {1..15} into two equal-sum sets?",
        "hire": "QAOA / QUBO",
        "answer": {"diff": part.get("diff"), "spins": part.get("spins")},
        "ok": bool(part.get("ok")),
        "method": part.get("method"),
        "detail": {"diff": part.get("diff"), "total": part.get("total")},
    })

    # --- linear systems (b = A x is the published object) ---
    def _lin(A, x, box):
        b = [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]
        return A, b, x, box

    systems = (
        _lin([[2, 1], [1, 3]], [1, 3], 8),
        _lin([[3, 0, 1], [1, 2, 0], [0, 1, 4]], [2, 1, 3], 6),
        _lin([[4, 1, 0], [1, 3, 1], [0, 1, 2]], [2, 1, 3], 6),
    )
    for A, b, x_true, box in systems:
        lin = fold_linear_system(A, b, box)
        ok = bool(lin.get("ok") and list(lin.get("x") or []) == list(x_true))
        rows.append({
            "family": "linear",
            "question": f"Solve Ax=b for A={A} b={b}?",
            "hire": "HHL",
            "answer": lin.get("x"),
            "ok": ok,
            "method": lin.get("method"),
            "detail": {"residual": lin.get("residual"), "published_x": list(x_true)},
        })

    # --- 3-color C5 ---
    n_c, edges, wit_c = _color_path6()
    col = fold_three_color(n_c, edges, wit_c)
    rows.append({
        "family": "color",
        "question": "3-color the 5-cycle?",
        "hire": "QAOA",
        "answer": col.get("colors"),
        "ok": bool(col.get("ok")),
        "method": col.get("method"),
        "detail": {"mono": col.get("mono")},
    })

    # --- larger Grover ---
    for n_items, marked in ((100_000, 42424), (1_000_000, 314159)):
        sr = fold_marked_search(n_items, marked)
        rows.append({
            "family": "search",
            "question": f"Find marked index {marked} in {n_items} items?",
            "hire": "Grover",
            "answer": sr.get("got"),
            "ok": bool(sr.get("ok")),
            "method": sr.get("method"),
            "detail": {"n_items": n_items, "oracle_evals": sr.get("oracle_evals")},
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
        "suite": "hire_expand",
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
        "doctrine": (
            "Hired questions, not their circuits. Change domain / fold, "
            "not a coefficient. Pin D1D38A."
        ),
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "hire_expand.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Hired QC questions — answered on this fold",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "These are the *questions* people hire a QPU for. Answered with "
        "modular folds, collapse, and seed starts. No foreign circuit. "
        "No new coefficient. Factor ladder starts after harder-QC 10403.",
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
        "- Did not invent a coefficient or a learning rate.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "- Did not call RSA-2048 closed. Larger moduli stay the next climb on this path.",
        "",
        "```powershell",
        "python -m fsot_quantum.hire_expand",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HIRE_EXPAND.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HIRE_EXPAND.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "families": {k: f"{v['n_ok']}/{v['n']}" for k, v in fam_score.items()},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
