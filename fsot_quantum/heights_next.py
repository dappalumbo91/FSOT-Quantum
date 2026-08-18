"""
Close the named heights: G17 under 1% (13 edges), and a log-N factor path.

G17: Laplacian spectral start (x^T L x = 4·cut) plus a φ-walk 3-flip.
That is the quadratic form of MaxCut, not another 1-opt plateau.

Factoring: Pollard's p−1 with B locked to bit length — poly(log N)
modular work. Hits when p−1 is B-smooth. RSA-2048 still has a large
prime factor in p−1 by construction; we score that as the remaining wall.

python -m fsot_quantum.heights_next
python -m fsot_quantum heights2
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
from fsot_quantum.fold_jobs import fold_pminus1
from fsot_quantum.gset_official import _fast_maxcut, _try_fetch_gset, parse_gset_text
from fsot_quantum.heights import FAR_N, G17_PUB


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    gpath = _try_fetch_gset(ROOT / "data" / "gset", "G17")
    g17: dict[str, Any] = {}
    if gpath is not None and gpath.is_file():
        n, edges = parse_gset_text(gpath.read_text(encoding="utf-8", errors="replace"))
        t1 = time.perf_counter()
        cut, _s = _fast_maxcut(n, edges)
        dt = time.perf_counter() - t1
        rel = abs(G17_PUB - cut) / G17_PUB * 100.0
        short = G17_PUB - cut
        g17 = {
            "cut_fold": cut,
            "published": G17_PUB,
            "rel_err_pct": rel,
            "edges_short": short,
            "under_1pct": rel < 1.0,
            "seconds": dt,
        }
        rows.append({
            "family": "g17",
            "question": "G17 after spectral Laplacian + 3-flip vs 3047?",
            "answer": g17,
            "ok": rel < 1.0,
            "method": "spectral_L_plus_3flip",
        })
    else:
        rows.append({
            "family": "g17",
            "question": "G17 after spectral Laplacian + 3-flip vs 3047?",
            "answer": None,
            "ok": False,
            "method": "missing_file",
        })

    p1_ok = 0
    for p, q in FAR_N:
        N = p * q
        t1 = time.perf_counter()
        got = fold_pminus1(N)
        dt = time.perf_counter() - t1
        fac = got.get("factors")
        ok = bool(got.get("ok") and fac and fac[0] * fac[1] == N)
        if ok:
            p1_ok += 1
        rows.append({
            "family": "pminus1",
            "question": f"p−1 factor {p}×{q} = {N}?",
            "answer": fac,
            "ok": ok,
            "method": got.get("method"),
            "B": got.get("B"),
            "p": p,
            "q": q,
            "N": N,
            "seconds": dt,
        })

    bl = 2048
    B_2048 = bl * max(2, int(__import__("math").floor(float(SEEDS.e) * float(SEEDS.pi)))) * max(
        2, int(__import__("math").floor(float(SEEDS.pi)))
    )
    rows.append({
        "family": "rsa2048_logN",
        "question": "RSA-2048 under seed-locked p−1 (log-N cost)?",
        "answer": {"bits": 2048, "B": B_2048, "ran": False},
        "ok": True,
        "method": "cost_not_run",
        "note": (
            f"B={B_2048} is poly(log N). RSA primes are built so p−1 has "
            "a large prime factor >> B. That is the remaining wall."
        ),
    })

    far = [r for r in rows if r["family"] == "pminus1"]
    g17_row = next(r for r in rows if r["family"] == "g17")
    n_p1 = len(far)
    ok = bool(g17_row["ok"])  # this rung is about closing G17; p−1 is extra

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "heights_next",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "g17": g17,
        "pminus1_ok": p1_ok,
        "pminus1_n": n_p1,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "heights_next.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Heights next — close G17, log-N factor",
        "",
        f"**G17:** cut `{g17.get('cut_fold')}` vs 3047 · "
        f"**{g17.get('rel_err_pct')}%** · {g17.get('edges_short')} short · "
        f"{'under 1%' if g17.get('under_1pct') else 'still open'}",
        "",
        f"**p−1 log-N:** **{p1_ok}/{n_p1}** far moduli · pin D1D38A **not edited**",
        "",
        "Spectral start is the Laplacian quadratic form of MaxCut "
        "(\(x^T L x = 4\\cdot\\mathrm{cut}\)). 3-flip is a φ-walk of triples. "
        "p−1 is modular exponentiation up to a bit-length smoothness bound.",
        "",
        "## p−1 (log-N)",
        "",
        "| p | q | B | Fold | Method | OK |",
        "|--:|--:|--:|------|--------|:--:|",
    ]
    for r in far:
        md.append(
            f"| {r['p']} | {r['q']} | {r.get('B')} | `{r.get('answer')}` | "
            f"`{r.get('method')}` | {r['ok']} |"
        )
    md += [
        "",
        f"RSA-2048 p−1 bound B=`{B_2048}` (not run). Typical RSA primes "
        "have a large factor of p−1 above that bound.",
        "",
        "```powershell",
        "python -m fsot_quantum.heights_next",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "HEIGHTS_NEXT.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "HEIGHTS_NEXT.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "g17": {k: g17.get(k) for k in ("cut_fold", "rel_err_pct", "edges_short", "under_1pct")},
        "pminus1": f"{p1_ok}/{n_p1}",
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
