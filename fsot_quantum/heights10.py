"""
Next real move: ECM at 64-bit far p±1-unsmooth.

heights9 was 56-bit. This board is ~9e8 × 2e10. Same B / B2,
same seed curves. Not RSA-2048.

python -m fsot_quantum.heights10
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

ECM10_N: tuple[tuple[int, int], ...] = (
    (900000053, 20000000089),
    (900000053, 20000000113),
    (900000053, 20000000117),
    (900000067, 20000000089),
    (900000067, 20000000113),
    (900000067, 20000000117),
    (900000131, 20000000089),
    (900000131, 20000000113),
)


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []
    ecm_ok = log_ok = 0
    for p, q in ECM10_N:
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

    n = len(ECM10_N)
    ok = ecm_ok == n
    bl = 2048
    B = bl * max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))) * max(
        2, int(math.floor(float(SEEDS.pi)))
    )
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights10",
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
    (out / "heights10.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Heights 10 — ECM at 64-bit far p±1-unsmooth",
        "",
        f"**ECM:** **{ecm_ok}/{n}** · log-N **{log_ok}/{n}**",
        "",
        "heights9 was 56-bit. This board is **64-bit** (`9e8 × 2e10`). "
        "Same B / B2, seed-locked curves. No new coefficient.",
        "",
        f"G17 remains `{G17_NOW}` vs 3047 (**{G17_PUB - G17_NOW} edges**). "
        "RSA-2048 still not run.",
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
        f"RSA-2048: B=`{B}` still (not run). 64-bit is not 2048-bit.",
        "",
        "```powershell",
        "python -m fsot_quantum.heights10",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS10.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS10.md").write_text(text, encoding="utf-8")
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
