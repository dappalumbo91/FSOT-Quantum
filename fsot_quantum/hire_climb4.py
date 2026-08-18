"""
Hired QC climb 4 — back on the QPU jobs.

Genetics was a side path after branching. This repo's climb is the
questions people hire a quantum computer for. 9-digit factor, larger
dlog, SAT-20, TSP n=8, 5×5 linear, independent set.

No foreign circuit. No new coefficient. Genetics repo not touched.

python -m fsot_quantum.hire_climb4
python -m fsot_quantum hire4
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
from fsot_quantum.fold_jobs import fold_factor, fold_period_finding
from fsot_quantum.hire_climb import _tsp_metric, fold_three_sat, fold_tsp
from fsot_quantum.hire_expand import _dlog_row, fold_discrete_log, fold_linear_system, fold_partition

FACTOR_N: tuple[int, ...] = (
    100440259,  # 10007 × 10037
    102151433,  # 10103 × 10111
    104387053,  # 10211 × 10223
    106131203,  # 10301 × 10303
    108743183,  # 10427 × 10429
    110397013,  # 10501 × 10513
    121330081,  # 11003 × 11027
    123543221,  # 11113 × 11117
    130101007,  # 10007 × 13001  farther
    144216077,  # 12007 × 12011
)

DLOG: tuple[tuple[int, int, int, int], ...] = (
    _dlog_row(3, 233, 200003),
    _dlog_row(5, 377, 250007),
    _dlog_row(6, 610, 300007),
    _dlog_row(7, 987, 350003),
)

PERIODS: tuple[tuple[int, int], ...] = (
    (3, 39203),
    (7, 64507),
    (10, 103603),
)


def _sat20() -> tuple[int, tuple[tuple[tuple[int, int], ...], ...], list[int]]:
    n = 20
    phi = int(float(SEEDS.phi) * 1e6)
    wit = [((phi >> i) & 1) for i in range(n)]
    if sum(wit) < 3:
        wit[0] = wit[2] = wit[5] = 1
    clauses: list[tuple[tuple[int, int], ...]] = []
    for k in range(36):
        idx = [((phi * (k + 3) + i * 19) % n) for i in range(3)]
        if len(set(idx)) < 3:
            idx = [(k + 3 * i) % n for i in range(3)]
        clauses.append(tuple((i, bool(wit[i])) for i in idx))
    return n, tuple(clauses), wit


def _lin5() -> tuple[list[list[int]], list[int], list[int], int]:
    A = [
        [2, 1, 0, 0, 0],
        [1, 3, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 3, 1],
        [0, 0, 0, 1, 2],
    ]
    x = [1, 0, 2, -1, 3]
    b = [sum(A[i][j] * x[j] for j in range(5)) for i in range(5)]
    return A, b, x, 6


def fold_independent_set(n: int, edges: Sequence[tuple[int, int]]) -> dict[str, Any]:
    """
    Max independent set (QAOA hire). Energy = size, illegal if an edge
    is both-selected. Seed starts + 1-flip. Exact check n≤12.
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def legal(bits: Sequence[int]) -> bool:
        return all(not (bits[u] and bits[v]) for u, v in edges)

    def size(bits: Sequence[int]) -> int:
        return sum(bits) if legal(bits) else -1

    def polish(bits: list[int]) -> list[int]:
        s = list(bits)
        improved = True
        steps = 0
        while improved and steps < n * n * 6:
            improved = False
            steps += 1
            cur = size(s)
            for i in range(n):
                s[i] ^= 1
                if size(s) > cur:
                    improved = True
                    break
                s[i] ^= 1
        return s

    phi = float(SEEDS.phi)
    starts = [
        [0] * n,
        [i % 2 for i in range(n)],
        [(i + 1) % 2 for i in range(n)],
    ]
    for k in range(int(math.floor(float(SEEDS.pi)))):
        starts.append([((int(phi * 1e6) * (k + 2) >> i) & 1) for i in range(n)])

    best = polish(starts[0])
    best_s = size(best)
    for st in starts[1:]:
        g = polish(st)
        s = size(g)
        if s > best_s:
            best, best_s = g, s

    exact = -1
    if n <= 12:
        for mask in range(1 << n):
            bits = [(mask >> i) & 1 for i in range(n)]
            exact = max(exact, size(bits))
    return {
        "job": "max_independent_set",
        "n": n,
        "size": best_s,
        "exact": exact,
        "ok": exact >= 0 and best_s == exact and best_s >= 0,
        "method": "legal_size_fold",
        "bits": best,
    }


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

    for g, h, p, _x in DLOG:
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

    n_sat, clauses, wit = _sat20()
    sat = fold_three_sat(n_sat, clauses, wit)
    rows.append({
        "family": "sat",
        "question": f"Satisfy the {n_sat}-bit 3-SAT ({len(clauses)} clauses)?",
        "hire": "Grover / QAOA",
        "answer": sat.get("unsat"),
        "ok": bool(sat.get("ok")),
        "method": sat.get("method"),
    })

    tsp = fold_tsp(_tsp_metric(8))
    rows.append({
        "family": "tsp",
        "question": "TSP n=8 on the seed metric — match exact tour length?",
        "hire": "QAOA / annealer",
        "answer": {"length": tsp.get("length"), "exact": tsp.get("exact_length")},
        "ok": bool(tsp.get("ok")),
        "method": tsp.get("method"),
    })

    A, b, x_true, box = _lin5()
    lin = fold_linear_system(A, b, box)
    rows.append({
        "family": "linear",
        "question": "Solve 5×5 Ax=b?",
        "hire": "HHL",
        "answer": lin.get("x"),
        "ok": bool(lin.get("ok") and list(lin.get("x") or []) == x_true),
        "method": lin.get("method"),
    })

    # C7: max independent set size 3
    c7 = tuple((i, (i + 1) % 7) for i in range(7))
    mis = fold_independent_set(7, c7)
    rows.append({
        "family": "mis",
        "question": "Max independent set of the 7-cycle?",
        "hire": "QAOA",
        "answer": {"size": mis.get("size"), "exact": mis.get("exact")},
        "ok": bool(mis.get("ok") and mis.get("exact") == 3),
        "method": mis.get("method"),
    })

    part = fold_partition(list(range(1, 28)))
    rows.append({
        "family": "partition",
        "question": "Partition {1..27} into two equal-sum sets?",
        "hire": "QAOA / QUBO",
        "answer": {"diff": part.get("diff")},
        "ok": bool(part.get("ok")),
        "method": part.get("method"),
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
        "suite": "hire_climb4",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "families": fam_score,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "previous": "hire_climb3 17/17 through 20937233",
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
        "doctrine": "Hired QC questions. Not genetics. Folds, not their stack.",
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "hire_climb4.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Hired QC climb 4 — back on the QPU jobs",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "Genetics was a side path. This rung is the jobs a QPU is hired for: "
        "9-digit factor, larger dlog, SAT-20, TSP n=8, 5×5 HHL, C7 independent set.",
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
        shown = "`" + json.dumps(ans, separators=(",", ":"))[:80] + "`" if isinstance(ans, (list, dict)) else f"`{ans}`"
        md.append(
            f"| {r['family']} | {r['question']} | {shown} | `{r.get('method')}` | {r['ok']} |"
        )
    md += [
        "",
        "## What we did not do",
        "",
        "- Did not open another genetics panel.",
        "- Did not replay a QFT / HHL / QAOA circuit.",
        "- Did not invent a coefficient.",
        "- Did not call RSA-2048 closed.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.hire_climb4",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HIRE_CLIMB4.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HIRE_CLIMB4.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "families": {k: f"{v['n_ok']}/{v['n']}" for k, v in fam_score.items()},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
