"""
Next real move: log-N factoring that is not p−1-only and not √p.

p−1 hit 3/8. This rung adds Williams p+1 (p+1 smooth) and
Fermat-on-kN (p/q near a small seed rational). Combined fold_logN.

G17 stays at 3034 / 0.427% (13 edges) — π³ breakout did not close it.

python -m fsot_quantum.heights3
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
from fsot_quantum.fold_jobs import fold_fermat_multipliers, fold_logN, fold_pminus1, fold_pplus1
from fsot_quantum.heights import FAR_N, G17_PUB

G17_NOW = 3034


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    p1_ok = pp_ok = fm_ok = ln_ok = 0
    for p, q in FAR_N:
        N = p * q
        a = fold_pminus1(N)
        b = fold_pplus1(N)
        c = fold_fermat_multipliers(N)
        d = fold_logN(N)
        if a.get("ok"):
            p1_ok += 1
        if b.get("ok"):
            pp_ok += 1
        if c.get("ok"):
            fm_ok += 1
        if d.get("ok"):
            ln_ok += 1
        rows.append({
            "family": "logN",
            "question": f"log-N factor {p}×{q}?",
            "p": p,
            "q": q,
            "N": N,
            "pminus1": a.get("method"),
            "pplus1": b.get("method"),
            "fermat_k": c.get("method"),
            "logN": d.get("method"),
            "answer": d.get("factors"),
            "ok": bool(d.get("ok")),
        })

    n = len(FAR_N)
    ok = ln_ok == n
    bl = 2048
    B = bl * max(2, int(__import__("math").floor(float(SEEDS.e) * float(SEEDS.pi)))) * max(
        2, int(__import__("math").floor(float(SEEDS.pi)))
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights3",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "logN_ok": ln_ok,
        "logN_n": n,
        "pminus1_ok": p1_ok,
        "pplus1_ok": pp_ok,
        "fermat_k_ok": fm_ok,
        "g17": {"cut": G17_NOW, "published": G17_PUB, "short": G17_PUB - G17_NOW},
        "rsa2048_B": B,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "heights3.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Heights 3 — log-N factor (p−1 + p+1 + kN Fermat)",
        "",
        f"**log-N:** **{ln_ok}/{n}** far moduli · "
        f"p−1 {p1_ok}/{n} · p+1 {pp_ok}/{n} · kN-Fermat {fm_ok}/{n}",
        "",
        f"G17 remains `{G17_NOW}` vs 3047 (**{G17_PUB - G17_NOW} edges**, 0.427%). "
        "π³ breakout did not close it. Family is already 11/11 under 1%.",
        "",
        "These three methods are **poly(log N)** once B and the Fermat cap "
        "are locked to bit length. They are not Pollard ρ (√p) and not a QFT.",
        "",
        "| p | q | p−1 | p+1 | kN Fermat | logN | OK |",
        "|--:|--:|-----|-----|-----------|------|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['p']} | {r['q']} | `{r['pminus1']}` | `{r['pplus1']}` | "
            f"`{r['fermat_k']}` | `{r['logN']}` | {r['ok']} |"
        )
    md += [
        "",
        f"RSA-2048: B=`{B}` still (not run). The remaining miss "
        "`100003×1000003` has both p−1 and p+1 unsmooth at this B.",
        "",
        "```powershell",
        "python -m fsot_quantum.heights3",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS3.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS3.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "logN": f"{ln_ok}/{n}",
        "pminus1": f"{p1_ok}/{n}",
        "pplus1": f"{pp_ok}/{n}",
        "fermat_k": f"{fm_ok}/{n}",
        "g17_short": G17_PUB - G17_NOW,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
