"""
RSA-100 — 330-bit public challenge, QS 1991. Living miss at locked B.

Public 330-bit challenge N (Lenstra et al., 1991, quadratic sieve).
Bitlen-locked B = bitlen · ⌊eπ⌋ · ⌊π⌋. Not a raised B. Pin D1D38A.
Do not look up p, q. End-job is SIQS at smoothness B2 (same stage-2
product as CFRAC 1-LP and ECM stage-2). Pollard ρ is not this lane:
cap would be ⌊π⌋·√N ~ 2^165.

python -m fsot_quantum.rsa100
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
    _stage2_bound,
    fold_cfrac,
    fold_ecm,
    fold_fermat_multipliers,
    fold_pminus1,
    fold_pplus1,
)
from fsot_quantum.fold_siqs import fold_siqs
from fsot_quantum.heights import G17_PUB

G17_NOW = 3047

# RSA-100, decimal, public challenge. Factors are not stored here.
RSA100_N = int(
    "1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139"
)


def _B_of(N: int) -> tuple[int, int, int, int]:
    bl = max(N.bit_length(), 8)
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    P = max(2, int(math.floor(float(SEEDS.pi))))
    B = bl * L0 * P
    B2 = _stage2_bound(B)
    return bl, B, B2, _stage2_bound(B2)


def _run_lane(name: str, fn, N: int) -> dict[str, Any]:
    t0 = time.perf_counter()
    got = fn(N)
    got = dict(got)
    got["lane"] = name
    got["wall"] = time.perf_counter() - t0
    print(
        json.dumps(
            {
                "lane": name,
                "ok": got.get("ok"),
                "method": got.get("method"),
                "wall": got["wall"],
                "n_rels": got.get("n_rels"),
                "n_fb": got.get("n_fb"),
                "n_poly": got.get("n_poly"),
            },
            indent=2,
        ),
        flush=True,
    )
    return got


def main() -> int:
    t0 = time.perf_counter()
    N = RSA100_N
    bl, B, B2, cap = _B_of(N)
    print(
        json.dumps(
            {
                "N_digits": len(str(N)),
                "bitlen": bl,
                "B": B,
                "B2": B2,
                "cfrac_cap": cap,
                "pin": "D1D38A",
            },
            indent=2,
        ),
        flush=True,
    )
    lanes = [
        _run_lane("pminus1", fold_pminus1, N),
        _run_lane("pplus1", fold_pplus1, N),
        _run_lane("fermat", fold_fermat_multipliers, N),
        _run_lane("ecm", fold_ecm, N),
        _run_lane("cfrac", fold_cfrac, N),
        _run_lane("siqs", fold_siqs, N),
    ]
    hit = next((r for r in lanes if r.get("ok")), None)
    ok = hit is not None
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "rsa100",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "B_raised": False,
        "factors_looked_up": False,
        "overall_ok": ok,
        "N": str(N),
        "bitlen": bl,
        "B": B,
        "B2": B2,
        "cfrac_cap": cap,
        "rho_skipped": "cap is floor(pi)*isqrt(N) ~ 2^165; not the RSA-100 lane",
        "g17": {"cut": G17_NOW, "published": G17_PUB, "short": G17_PUB - G17_NOW},
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "wall_seconds": time.perf_counter() - t0,
        "hit": None
        if hit is None
        else {
            "lane": hit.get("lane"),
            "method": hit.get("method"),
            "factors_bits": [int(f).bit_length() for f in hit.get("factors") or []],
        },
        "lanes": [
            {
                "lane": r.get("lane"),
                "ok": r.get("ok"),
                "method": r.get("method"),
                "wall": r.get("wall"),
                "B": r.get("B"),
                "B2": r.get("B2"),
                "n_rels": r.get("n_rels"),
                "need": r.get("need"),
                "n_fb": r.get("n_fb"),
                "n_poly": r.get("n_poly"),
                "n_scan": r.get("n_scan"),
                "n_triv": r.get("n_triv"),
                "steps": r.get("steps"),
            }
            for r in lanes
        ],
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "rsa100.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    end = hit.get("method") if hit else lanes[-1].get("method")
    md = [
        "# RSA-100 — 330-bit public challenge",
        "",
        f"**{'hit' if ok else 'miss'}** · pin D1D38A **not edited** · B **not raised** · factors **not looked up**",
        "",
        f"N is the public RSA-100 modulus ({bl}-bit). Locked "
        f"B = bitlen · ⌊eπ⌋ · ⌊π⌋ = `{B}`. B2 = `{B2}`. "
        "End-job is SIQS at smoothness B2 (same stage-2 product as CFRAC "
        "1-LP and ECM stage-2). Pollard ρ is not this lane.",
        "",
        "See `docs/CLASSICAL_RECORDS.md`.",
        "",
        f"G17 remains `{G17_NOW}` vs 3047 (**{G17_PUB - G17_NOW} edges**).",
        "",
        "| Lane | method | ok | wall s |",
        "|------|--------|:--:|-------:|",
    ]
    for r in lanes:
        md.append(
            f"| `{r.get('lane')}` | `{r.get('method')}` | {r.get('ok')} | "
            f"{r.get('wall', 0):.3f} |"
        )
    md += [
        "",
        f"End: `{end}`.",
        "",
        "```powershell",
        "python -m fsot_quantum.rsa100",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "RSA100.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "RSA100.md").write_text(text, encoding="utf-8")
    print(
        json.dumps(
            {
                "overall_ok": ok,
                "end": end,
                "B": B,
                "B2": B2,
                "wall_seconds": report["wall_seconds"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
