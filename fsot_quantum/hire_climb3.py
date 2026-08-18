"""
Hired QC climb 3 — 8-digit factors and larger discrete log.

After hire2 (7-digit through 2196323, dlog p=40009). Same fold law.
No foreign circuit. No new coefficient.

python -m fsot_quantum.hire_climb3
python -m fsot_quantum hire3
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

from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_jobs import fold_factor, fold_period_finding
from fsot_quantum.hire_expand import _dlog_row, fold_discrete_log

FACTOR_N: tuple[int, ...] = (
    10400609,  # 3221 × 3229
    10575503,  # 3251 × 3253
    10936213,  # 3301 × 3313
    12006221,  # 3463 × 3467
    12348187,  # 3511 × 3517
    12787751,  # 3571 × 3581
    16016003,  # 4001 × 4003
    17040383,  # 4127 × 4129
    16114663,  # 3221 × 5003  (farther pair)
    20937233,  # 4001 × 5233
)

DLOG: tuple[tuple[int, int, int, int], ...] = (
    _dlog_row(3, 144, 50021),
    _dlog_row(5, 233, 70001),
    _dlog_row(6, 377, 90001),
    _dlog_row(7, 610, 100003),
)

PERIODS: tuple[tuple[int, int], ...] = (
    (3, 10403),
    (5, 6557),
    (10, 8633),
)


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
        "suite": "hire_climb3",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "families": fam_score,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "previous": "hire_climb 32/32 through 2196323",
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "hire_climb3.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Hired QC climb 3 — 8-digit factors",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "After `hire2` (7-digit). Same modular fold. Factors through "
        "**20,937,233**. Discrete log through **p = 100003**.",
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
        md.append(
            f"| {r['family']} | {r['question']} | `{r.get('answer')}` | `{r.get('method')}` | {r['ok']} |"
        )
    md += [
        "",
        "## What we did not do",
        "",
        "- Did not replay a QFT circuit.",
        "- Did not invent a coefficient.",
        "- Did not call RSA-2048 closed.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.hire_climb3",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HIRE_CLIMB3.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HIRE_CLIMB3.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "families": {k: f"{v['n_ok']}/{v['n']}" for k, v in fam_score.items()},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
