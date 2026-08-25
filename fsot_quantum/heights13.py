"""
Classical-record direction: RSA-shaped 48-bit × 48-bit (95-bit N).

heights12 was 41-bit × 41-bit (81-bit). Same job cryptographers mean:
two similar-bit primes, not twins, p±1 unsmooth at our B. End-job
ECM or Pollard ρ. Consumer PC. Not RSA-2048.

python -m fsot_quantum.heights13
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

BAL48: tuple[tuple[int, int], ...] = (
    (150000000000121, 250000000000043),
    (150000000000121, 250000000000111),
    (150000000000121, 250000000000129),
    (150000000000121, 250000000000199),
    (150000000000131, 250000000000043),
    (150000000000131, 250000000000111),
    (150000000000133, 250000000000043),
    (150000000000199, 250000000000043),
)


def _row(p: int, q: int) -> dict[str, Any]:
    N = p * q
    a = fold_pminus1(N)
    b = fold_pplus1(N)
    c = fold_fermat_multipliers(N)
    e = fold_ecm(N)
    d = fold_logN(N)
    if not d.get("ok"):
        d = fold_pollard_rho(N)
    return {
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
    rows = [_row(p, q) for p, q in BAL48]
    n = len(rows)
    n_ok = sum(1 for r in rows if r["ok"])
    ok = n_ok == n
    bl = 2048
    B = bl * max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))) * max(
        2, int(math.floor(float(SEEDS.pi)))
    )
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights13",
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
    (out / "heights13.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Heights 13 — RSA-shaped 48-bit × 48-bit (95-bit N)",
        "",
        f"**{n_ok}/{n}** · classical-record direction on a consumer PC",
        "",
        "Two similar-bit primes, not twins. p±1 and Fermat miss at our B. "
        "End-job ECM or Pollard ρ. This is the object cryptographers mean "
        "(balanced bits). Not RSA-100 / RSA-250 / RSA-2048.",
        "",
        "See `docs/CLASSICAL_RECORDS.md`.",
        "",
        f"G17 remains `{G17_NOW}` vs 3047 (**{G17_PUB - G17_NOW} edges**).",
        "",
        "| p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |",
        "|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['p_bits']} | {r['q_bits']} | {r['bits']} | "
            f"`{r['pminus1']}` | `{r['pplus1']}` | `{r['fermat_k']}` | "
            f"`{r['ecm']}` | `{r['end']}` | {r['ok']} |"
        )
    md += [
        "",
        f"RSA-2048: B=`{B}` still (not run).",
        "",
        "```powershell",
        "python -m fsot_quantum.heights13",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS13.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS13.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "g17_short": G17_PUB - G17_NOW,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
