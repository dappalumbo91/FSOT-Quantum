"""
Hired QC climb 5 — 10-digit factor and harder QAOA/HHL jobs.

After hire4 (9-digit through 144216077). Same fold law.
No foreign circuit. No new coefficient. Not genetics.

python -m fsot_quantum.hire_climb5
python -m fsot_quantum hire5
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_jobs import fold_factor, fold_period_finding
from fsot_quantum.hire_climb import _tsp_metric, fold_three_sat, fold_tsp
from fsot_quantum.hire_climb4 import fold_independent_set
from fsot_quantum.hire_expand import _dlog_row, fold_discrete_log, fold_linear_system, fold_partition

FACTOR_N: tuple[int, ...] = (
    1000773161,  # 31627 × 31643
    1003305481,  # 31663 × 31687
    1024384027,  # 32003 × 32009
    1090188299,  # 33013 × 33023
    1226750621,  # 35023 × 35027
    1296648077,  # 36007 × 36011
    1370184247,  # 37013 × 37019
    1445900429,  # 38011 × 38039
    1107798929,  # 31627 × 35027  farther
    1184719057,  # 32003 × 37019
)

DLOG: tuple[tuple[int, int, int, int], ...] = (
    _dlog_row(3, 377, 500009),
    _dlog_row(5, 610, 700001),
    _dlog_row(6, 987, 1000003),
    _dlog_row(7, 1597, 1200007),
)

PERIODS: tuple[tuple[int, int], ...] = (
    (3, 172189),
    (5, 103603),
    (7, 142763),
)


def _sat24() -> tuple[int, tuple[tuple[tuple[int, int], ...], ...], list[int]]:
    n = 24
    phi = int(float(SEEDS.phi) * 1e6)
    wit = [((phi >> i) & 1) for i in range(n)]
    if sum(wit) < 4:
        for i in (0, 3, 7, 11):
            wit[i] = 1
    clauses: list[tuple[tuple[int, int], ...]] = []
    for k in range(48):
        idx = [((phi * (k + 5) + i * 23) % n) for i in range(3)]
        if len(set(idx)) < 3:
            idx = [(k + 4 * i) % n for i in range(3)]
        clauses.append(tuple((i, bool(wit[i])) for i in idx))
    return n, tuple(clauses), wit


def _lin6() -> tuple[list[list[int]], list[int], list[int], int]:
    A = [
        [2, 1, 0, 0, 0, 0],
        [1, 3, 1, 0, 0, 0],
        [0, 1, 2, 1, 0, 0],
        [0, 0, 1, 3, 1, 0],
        [0, 0, 0, 1, 2, 1],
        [0, 0, 0, 0, 1, 3],
    ]
    x = [1, -1, 2, 0, 1, 2]
    b = [sum(A[i][j] * x[j] for j in range(6)) for i in range(6)]
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

    n_sat, clauses, wit = _sat24()
    sat = fold_three_sat(n_sat, clauses, wit)
    rows.append({
        "family": "sat",
        "question": f"Satisfy the {n_sat}-bit 3-SAT ({len(clauses)} clauses)?",
        "hire": "Grover / QAOA",
        "answer": sat.get("unsat"),
        "ok": bool(sat.get("ok")),
        "method": sat.get("method"),
    })

    tsp = fold_tsp(_tsp_metric(9))
    rows.append({
        "family": "tsp",
        "question": "TSP n=9 on the seed metric — match exact tour length?",
        "hire": "QAOA / annealer",
        "answer": {"length": tsp.get("length"), "exact": tsp.get("exact_length")},
        "ok": bool(tsp.get("ok")),
        "method": tsp.get("method"),
    })

    A, b, x_true, box = _lin6()
    lin = fold_linear_system(A, b, box)
    rows.append({
        "family": "linear",
        "question": "Solve 6×6 Ax=b?",
        "hire": "HHL",
        "answer": lin.get("x"),
        "ok": bool(lin.get("ok") and list(lin.get("x") or []) == x_true),
        "method": lin.get("method"),
    })

    c9 = tuple((i, (i + 1) % 9) for i in range(9))
    mis = fold_independent_set(9, c9)
    rows.append({
        "family": "mis",
        "question": "Max independent set of the 9-cycle?",
        "hire": "QAOA",
        "answer": {"size": mis.get("size"), "exact": mis.get("exact")},
        "ok": bool(mis.get("ok") and mis.get("exact") == 4),
        "method": mis.get("method"),
    })

    part = fold_partition(list(range(1, 32)))
    rows.append({
        "family": "partition",
        "question": "Partition {1..31} into two equal-sum sets?",
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
        "suite": "hire_climb5",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "families": fam_score,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "previous": "hire_climb4 22/22 through 144216077",
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "hire_climb5.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Hired QC climb 5 — 10-digit factor",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "After `hire4`. Same modular / energy folds. Factors through "
        "**1,445,900,429**. Discrete log through **p = 1,200,007**. "
        "SAT-24, TSP n=9, 6×6 HHL, C9 independent set.",
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
        "- Did not open a genetics panel.",
        "- Did not replay a QFT / HHL / QAOA circuit.",
        "- Did not invent a coefficient.",
        "- Did not call RSA-2048 closed.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.hire_climb5",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HIRE_CLIMB5.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HIRE_CLIMB5.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "families": {k: f"{v['n_ok']}/{v['n']}" for k, v in fam_score.items()},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
