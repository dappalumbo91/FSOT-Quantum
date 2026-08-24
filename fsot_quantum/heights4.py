"""
Next real move on the RSA wall: ECM after p±1 and kN Fermat miss.

Far primes whose p−1 and p+1 are both unsmooth at the bitlen-locked
B2. Fermat cannot hit them. Lenstra ECM, same B / B2, seed curves.

G17 stays 3034 / 13 edges — full zero-ridge exact (2^27) did not move it.
The remaining 13 require negative-gain flips. Written, not crawled.

python -m fsot_quantum.heights4
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

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import domain_scalar
from fsot_quantum.fold_jobs import (
    fold_ecm,
    fold_fermat_multipliers,
    fold_logN,
    fold_pminus1,
    fold_pplus1,
)
from fsot_quantum.heights import G17_PUB

G17_NOW = 3034

# Far, both p±1 unsmooth at B2, not Fermat-close.
ECM_N: tuple[tuple[int, int], ...] = (
    (140683, 1000289),
    (140683, 1000291),
    (140683, 1000423),
    (142123, 1000289),
    (143357, 1000289),
    (144427, 1000289),
    (146347, 1000289),
    (146837, 1000289),
)


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []
    ecm_ok = log_ok = 0
    for p, q in ECM_N:
        N = p * q
        a = fold_pminus1(N)
        b = fold_pplus1(N)
        c = fold_fermat_multipliers(N)
        e = fold_ecm(N)
        d = fold_logN(N)
        if e.get("ok"):
            ecm_ok += 1
        if d.get("ok"):
            log_ok += 1
        rows.append({
            "p": p,
            "q": q,
            "N": N,
            "bits": N.bit_length(),
            "pminus1": a.get("method"),
            "pplus1": b.get("method"),
            "fermat_k": c.get("method"),
            "ecm": e.get("method"),
            "logN": d.get("method"),
            "factors": d.get("factors"),
            "ok": bool(d.get("ok")),
        })

    n = len(ECM_N)
    ok = ecm_ok == n
    bl = 2048
    B = bl * max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))) * max(
        2, int(math.floor(float(SEEDS.pi)))
    )

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights4",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "ecm_ok": ecm_ok,
        "ecm_n": n,
        "logN_ok": log_ok,
        "g17": {"cut": G17_NOW, "published": G17_PUB, "short": G17_PUB - G17_NOW},
        "rsa2048_B": B,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "heights4.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Heights 4 — ECM on p±1-unsmooth far moduli",
        "",
        f"**ECM:** **{ecm_ok}/{n}** · log-N (p±1 + kN + ECM) **{log_ok}/{n}**",
        "",
        f"G17 remains `{G17_NOW}` vs 3047 (**{G17_PUB - G17_NOW} edges**, 0.427%). "
        "Exact fold of the full 27-vertex zero-gain ridge did not move it. "
        "The leftover 13 edges require negative-gain flips. Not crawled.",
        "",
        "These moduli are the RSA-shaped leftover after stage-2: both p−1 "
        "and p+1 unsmooth at B2, primes far apart so kN-Fermat misses. "
        "ECM uses the **same** B / B2 and seed-locked curves. "
        "No new coefficient. Not a QFT.",
        "",
        "| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |",
        "|--:|--:|-----:|-----|-----|----|-----|------|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['p']} | {r['q']} | {r['bits']} | `{r['pminus1']}` | "
            f"`{r['pplus1']}` | `{r['fermat_k']}` | `{r['ecm']}` | "
            f"`{r['logN']}` | {r['ok']} |"
        )
    md += [
        "",
        f"RSA-2048: B=`{B}` still (not run). ECM is the next smoothness "
        "lane, not a 2048-bit factor.",
        "",
        "```powershell",
        "python -m fsot_quantum.heights4",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS4.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS4.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "ecm": f"{ecm_ok}/{n}",
        "logN": f"{log_ok}/{n}",
        "g17_short": G17_PUB - G17_NOW,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
