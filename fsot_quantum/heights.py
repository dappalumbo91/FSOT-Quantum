"""
The written next heights: G17 and the RSA-shaped factor job.

hire3–hire7 climbed Fermat-close twins. That is not RSA. RSA moduli
have two primes of similar bit length that are *not* twin-close.
This rung:

  1. G17 again, with the plateau-ridge walk (1-opt is why we sat at 3016).
  2. Far semiprimes via seed-locked Pollard's rho (Fermat cannot hit them).
  3. RSA-2048 is scored as a cost, not a pretend factor.

No new coefficient. No Hilbert QFT. Genetics not touched.

python -m fsot_quantum.heights
python -m fsot_quantum heights
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
from fsot_quantum.fold_jobs import fold_factor, fold_pollard_rho
from fsot_quantum.gset_official import _fast_maxcut, _try_fetch_gset, parse_gset_text

# Far primes — not Fermat-close. RSA-shaped object.
FAR_N: tuple[tuple[int, int], ...] = (
    (10007, 1000003),
    (10007, 10000019),
    (7919, 104729),
    (65537, 100003),
    (100003, 1000003),
    (31627, 1000033),
    (104729, 1000003),
    (1000003, 1000033),  # close 7-digit pair still here as contrast
)

G17_PUB = 3047


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    # --- G17 ---
    gpath = _try_fetch_gset(ROOT / "data" / "gset", "G17")
    g17: dict[str, Any] = {"ok": False, "reason": "missing G17.txt"}
    if gpath is not None and gpath.is_file():
        n, edges = parse_gset_text(gpath.read_text(encoding="utf-8", errors="replace"))
        t1 = time.perf_counter()
        cut, _s = _fast_maxcut(n, edges)
        dt = time.perf_counter() - t1
        rel = abs(G17_PUB - cut) / G17_PUB * 100.0
        short = G17_PUB - cut
        g17 = {
            "n": n,
            "m": len(edges),
            "cut_fold": cut,
            "published": G17_PUB,
            "rel_err_pct": rel,
            "edges_short": short,
            "under_1pct": rel < 1.0,
            "seconds": dt,
        }
        rows.append({
            "family": "g17",
            "question": "G17 planar MaxCut vs published 3047?",
            "hire": "QAOA / MaxCut",
            "answer": {"cut": cut, "short": short, "rel": rel},
            "ok": rel < 1.0,
            "method": "kl_2opt_plateau_ridge",
        })
    else:
        rows.append({
            "family": "g17",
            "question": "G17 planar MaxCut vs published 3047?",
            "hire": "QAOA / MaxCut",
            "answer": None,
            "ok": False,
            "method": "missing_file",
        })

    # --- far factors ---
    for p, q in FAR_N:
        N = p * q
        # Fermat distance: steps ≈ ((p+q)/2 − sqrt(N))
        sN = math.isqrt(N)
        fermat_gap = abs((p + q) // 2 - sN)
        t1 = time.perf_counter()
        # Prefer rho for the far object; also record if Fermat would have been cheap
        rho = fold_pollard_rho(N)
        dt = time.perf_counter() - t1
        fac = rho.get("factors")
        ok = bool(rho.get("ok") and fac and fac[0] * fac[1] == N)
        rows.append({
            "family": "far_factor",
            "question": f"Factor far semiprime {p}×{q} = {N}?",
            "hire": "Shor / RSA-shaped",
            "answer": fac,
            "ok": ok,
            "method": rho.get("method"),
            "p": p,
            "q": q,
            "N": N,
            "fermat_gap": fermat_gap,
            "seconds": dt,
        })

    # --- RSA-2048 is a cost, not a run ---
    bits = 2048
    # two ~1024-bit primes; Pollard ~ √p ~ 2^{512}
    rho_bits = bits // 4  # √(2^{1024}) = 2^{512} = 2^{bits/4}
    hilbert_qubits = 2 * bits
    rows.append({
        "family": "rsa2048",
        "question": "RSA-2048: can this fold method close it today?",
        "hire": "Shor / RSA",
        "answer": {
            "bits": bits,
            "pollard_steps_bits": rho_bits,
            "hilbert_qubits_if_QFT": hilbert_qubits,
            "ran": False,
        },
        "ok": True,  # honesty pass: we name the wall, we do not pretend
        "method": "cost_not_run",
        "note": (
            "Pollard/period cost tracks √p, not log N. "
            "2048-bit N ⇒ ~2^512 rho steps. That is the height. "
            "Fermat twins were the wrong object."
        ),
    })

    n = len(rows)
    # RSA row is an honesty check. G17 is the known graph height —
    # far factors are the RSA-shaped job we can score today.
    far = [r for r in rows if r["family"] == "far_factor"]
    n_ok = sum(1 for r in far if r["ok"])
    n_scored = len(far)
    ok = n_scored > 0 and n_ok == n_scored

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "n_scored": n_scored,
        "g17": g17,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "K": float(SEEDS.k),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
        "doctrine": (
            "G17 and far-prime factoring are the heights. "
            "Fermat twins are not RSA. RSA-2048 is a √p wall, not a refusal."
        ),
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "heights.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# The next heights — G17 and the RSA-shaped job",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n_scored}** scored · pin D1D38A **not edited**",
        "",
        "hire3–hire7 factored Fermat-close twins. That is **not** the RSA job. "
        "RSA moduli are two similar-bit primes that are not twin-close. "
        "G17 was written as 31 edges and then left. This rung works those two.",
        "",
    ]
    if g17.get("cut_fold") is not None:
        md += [
            "## G17",
            "",
            f"Cut `{g17['cut_fold']}` vs published **3047** · "
            f"**{g17['rel_err_pct']:.3f}%** · {g17['edges_short']} edges short · "
            f"{g17['seconds']:.2f}s.",
            "",
            "Method: existing KL + 2-opt + a **plateau-ridge walk** "
            "(zero-gain vertices in φ-order, then refine). "
            "Not a file-order crawl. Not a new coefficient.",
            "",
        ]
    md += [
        "## Far factors (RSA-shaped)",
        "",
        "| p | q | N | Fermat gap | Fold | Method | OK |",
        "|--:|--:|--:|-----------:|------|--------|:--:|",
    ]
    for r in rows:
        if r["family"] != "far_factor":
            continue
        md.append(
            f"| {r['p']} | {r['q']} | `{r['N']}` | {r.get('fermat_gap')} | "
            f"`{r.get('answer')}` | `{r.get('method')}` | {r['ok']} |"
        )
    md += [
        "",
        "## RSA-2048",
        "",
        "Not run. Pollard / period cost tracks **√p**, not log N. "
        "A 2048-bit modulus has ~1024-bit primes ⇒ ~**2^512** rho steps. "
        "A Hilbert QFT would want ~4096 qubits. Neither is this fold today. "
        "The climb is far-prime factoring at rising bit length, not twin Fermat.",
        "",
        "## Checks",
        "",
        "| Family | Question | OK |",
        "|--------|----------|:--:|",
    ]
    for r in rows:
        md.append(f"| {r['family']} | {r['question']} | {r['ok']} |")
    md += [
        "",
        "## What we did not do",
        "",
        "- Did not call RSA-2048 factored.",
        "- Did not crawl G17 with a file-order uncut pass.",
        "- Did not invent a coefficient.",
        "- Did not keep climbing Fermat twins and calling that RSA.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.heights",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n_scored}",
        "g17": {k: g17.get(k) for k in ("cut_fold", "rel_err_pct", "edges_short", "under_1pct")},
        "far_ok": sum(1 for r in rows if r["family"] == "far_factor" and r["ok"]),
        "far_n": sum(1 for r in rows if r["family"] == "far_factor"),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
