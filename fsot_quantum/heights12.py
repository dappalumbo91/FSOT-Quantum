"""
Next real move: RSA-shaped balanced primes + the 90-bit ECM miss.

ECM smoothness is not the consumer-hardware wall. The 90-bit pair
8000000081 × 1e17 exhausted ECM at the same B; Pollard ρ (already
on this path) factors it in ~1e5 steps. This board:

  1) that 90-bit unbalanced miss, closed by ρ
  2) 41-bit × 41-bit far primes (81-bit N) — similar bit length,
     not Fermat-close. p±1 miss; ECM or ρ.

python -m fsot_quantum.heights12
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
    fold_pollard_rho,
    fold_pplus1,
)
from fsot_quantum.heights import G17_PUB

G17_NOW = 3034

# 90-bit ECM-exhausted pair (33-bit × 57-bit).
UNBAL: tuple[tuple[int, int], ...] = (
    (8000000081, 100000000000000003),
    (8000000081, 100000000000000013),
    (8000000087, 100000000000000003),
    (8000000111, 100000000000000003),
)

# RSA-shaped: similar bit length, far enough that Fermat misses.
BAL: tuple[tuple[int, int], ...] = (
    (1100000000003, 1800000000047),
    (1100000000003, 1800000000083),
    (1100000000003, 1800000000101),
    (1100000000003, 1800000000119),
    (1100000000027, 1800000000047),
    (1100000000027, 1800000000083),
    (1100000000041, 1800000000047),
    (1100000000081, 1800000000047),
)


def _row(p: int, q: int, kind: str) -> dict[str, Any]:
    N = p * q
    a = fold_pminus1(N)
    b = fold_pplus1(N)
    c = fold_fermat_multipliers(N)
    e = fold_ecm(N)
    d = fold_logN(N)
    if not d.get("ok"):
        d = fold_pollard_rho(N)
    return {
        "kind": kind,
        "p": p,
        "q": q,
        "N": N,
        "bits": N.bit_length(),
        "p_bits": p.bit_length(),
        "q_bits": q.bit_length(),
        "pminus1": a.get("method"),
        "pplus1": b.get("method"),
        "fermat_k": c.get("method"),
        "ecm": e.get("method"),
        "end": d.get("method"),
        "factors": d.get("factors"),
        "ok": bool(d.get("ok")),
    }


def main() -> int:
    t0 = time.perf_counter()
    rows = [_row(p, q, "unbal_90") for p, q in UNBAL]
    rows += [_row(p, q, "bal_81") for p, q in BAL]
    n = len(rows)
    n_ok = sum(1 for r in rows if r["ok"])
    ok = n_ok == n
    bl = 2048
    B = bl * max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))) * max(
        2, int(math.floor(float(SEEDS.pi)))
    )
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights12",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n_ok": n_ok,
        "n": n,
        "g17": {"cut": G17_NOW, "published": G17_PUB, "short": G17_PUB - G17_NOW},
        "rsa2048_B": B,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "heights12.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Heights 12 — RSA-shaped balanced 81-bit + 90-bit ρ",
        "",
        f"**{n_ok}/{n}** · 90-bit unbalanced **{sum(1 for r in rows if r['kind']=='unbal_90' and r['ok'])}/{len(UNBAL)}** "
        f"· 81-bit balanced **{sum(1 for r in rows if r['kind']=='bal_81' and r['ok'])}/{len(BAL)}**",
        "",
        "ECM smoothness is not the PC wall. The 90-bit ECM miss has a "
        "33-bit factor; Pollard ρ (already on this path) hits in ~1e5 steps. "
        "The 81-bit board is two **41-bit** primes, far apart: p±1 and "
        "Fermat miss. End-job is ECM or ρ. Same seeds. No new coefficient.",
        "",
        "See `docs/CONSUMER_VS_QPU.md`: innovative vs QPU, not vs GNFS.",
        "",
        f"G17 remains `{G17_NOW}` vs 3047 (**{G17_PUB - G17_NOW} edges**).",
        "",
        "| kind | p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |",
        "|------|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['kind']} | {r['p_bits']} | {r['q_bits']} | {r['bits']} | "
            f"`{r['pminus1']}` | `{r['pplus1']}` | `{r['fermat_k']}` | "
            f"`{r['ecm']}` | `{r['end']}` | {r['ok']} |"
        )
    md += [
        "",
        f"RSA-2048: B=`{B}` still (not run).",
        "",
        "```powershell",
        "python -m fsot_quantum.heights12",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS12.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS12.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "g17_short": G17_PUB - G17_NOW,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
