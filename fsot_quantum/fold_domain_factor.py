"""
Domain-fold factor lane — the same 35-pin interface used on V_cb / H0 / Gset.

When a residual misses, FSOT changes domain / D_eff / lane, not a coefficient
and not a raised B. Physics leftovers were wrong objects. RSA-100 is the
hired factor question; the pin has no closed form for an artificial challenge
modulus. This lane re-asks that question at every preregistered D_eff:

  - Fermat multiplier k = D_eff (and products of two D_eff)
  - ECM curve a = D_eff, x0 from domain hits
  - Same bitlen-locked B / B2 as p−1 / ECM / SIQS

Not a look-up. Not a pin edit. Pin D1D38A.

python -m fsot_quantum.fold_domain_factor
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
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.fold_complexity import fold_depth_ladder, fold_probe_budget
from fsot_quantum.fold_jobs import (
    _ec_mul,
    _primes_upto,
    _stage2_bound,
    fold_ecm,
    fold_fermat_multipliers,
    fold_logN,
    fold_pminus1,
    fold_pplus1,
)
from fsot_quantum.rsa100 import RSA100_N


def _B_of(N: int) -> tuple[int, int, int]:
    bl = max(N.bit_length(), 8)
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    P = max(2, int(math.floor(float(SEEDS.pi))))
    B = bl * L0 * P
    return bl, B, _stage2_bound(B)


def _domain_ks() -> list[int]:
    """Unique pin D_eff and pairwise products — pin fields, not a fit."""
    deffs = sorted({int(d.D_eff) for d in DOMAINS.values() if int(d.D_eff) >= 1})
    ks = set(deffs)
    for i, a in enumerate(deffs):
        for b in deffs[i:]:
            ks.add(a * b)
    seed_ks = (
        1,
        2,
        max(2, int(math.floor(float(SEEDS.pi)))),
        max(2, int(math.floor(float(SEEDS.e)))),
        max(2, int(math.floor(float(SEEDS.phi)))),
    )
    ks.update(seed_ks)
    return sorted(ks)


def _fermat_k(N: int, k: int, cap: int) -> dict[str, Any] | None:
    M = k * N
    a0 = int(math.isqrt(M)) + 1
    for step in range(min(cap, M)):
        aa = a0 + step
        bb2 = aa * aa - M
        bb = int(math.isqrt(bb2))
        if bb * bb == bb2 and bb > 0:
            g = math.gcd(aa - bb, N)
            if 1 < g < N:
                return {
                    "job": "factor_Shor_end",
                    "N": N,
                    "ok": True,
                    "factors": sorted([g, N // g]),
                    "method": "domain_fermat",
                    "k": k,
                    "steps": step,
                }
    return None


def _ecm_curve(N: int, a: int, x0: int, B: int, B2: int, primes: list[int]) -> dict[str, Any] | None:
    y0 = 1
    pt: tuple[int, int] | None = (x0 % N, y0 % N)
    for q in primes:
        if q > B:
            break
        qe = q
        while qe * q <= B:
            qe *= q
        if pt is None:
            return None
        pt, fac = _ec_mul(qe, pt, a, N)
        if fac is not None and 1 < fac < N:
            return {
                "job": "factor_Shor_end",
                "N": N,
                "ok": True,
                "factors": sorted([fac, N // fac]),
                "method": "domain_ecm_stage1",
                "B": B,
                "B2": B2,
                "a": a,
            }
    if pt is None:
        return None
    for q in primes:
        if q <= B:
            continue
        _, fac = _ec_mul(q, pt, a, N)
        if fac is not None and 1 < fac < N:
            return {
                "job": "factor_Shor_end",
                "N": N,
                "ok": True,
                "factors": sorted([fac, N // fac]),
                "method": "domain_ecm_stage2",
                "B": B,
                "B2": B2,
                "a": a,
                "q": q,
            }
    return None


def fold_domain_factor(N: int) -> dict[str, Any]:
    """
    35-domain Fermat + ECM at locked B. Returns the same job dict as fold_cfrac.
    """
    if N < 4 or N % 2 == 0:
        from fsot_quantum.fold_jobs import fold_factor

        return fold_factor(N)
    bl, B, B2 = _B_of(N)
    cap = fold_probe_budget(max(bl, 8), fold_depth_ladder()["deep"]) * max(1, bl)

    for fn in (fold_pminus1, fold_pplus1, fold_fermat_multipliers, fold_ecm):
        got = fn(N)
        if got.get("ok"):
            got = dict(got)
            got["domain_lane"] = "existing_" + str(got.get("method"))
            return got

    n_fermat = 0
    for k in _domain_ks():
        n_fermat += 1
        hit = _fermat_k(N, k, cap)
        if hit is not None:
            hit["B"] = B
            hit["B2"] = B2
            hit["n_fermat_k"] = n_fermat
            return hit

    primes = _primes_upto(B2)
    n_curves = 0
    seen: set[tuple[int, int]] = set()
    for name, d in DOMAINS.items():
        a = int(d.D_eff)
        x0 = 2 + int(d.hits)
        if (a, x0) in seen:
            continue
        seen.add((a, x0))
        n_curves += 1
        hit = _ecm_curve(N, a, x0, B, B2, primes)
        if hit is not None:
            hit["domain"] = name
            hit["S"] = domain_scalar(name)
            hit["n_curves"] = n_curves
            return hit

    return {
        "job": "factor_Shor_end",
        "N": N,
        "ok": False,
        "factors": None,
        "method": "domain_factor_exhausted",
        "B": B,
        "B2": B2,
        "n_fermat_k": n_fermat,
        "n_curves": n_curves,
        "note": (
            "35 pin D_eff as Fermat k and ECM a, same B. "
            "RSA challenge moduli are not pin observables; S(domain) does not encode p, q."
        ),
    }


def main() -> int:
    t0 = time.perf_counter()
    smoke_n = 1000000007 * 1000000009
    smoke = fold_domain_factor(smoke_n)
    print(
        json.dumps(
            {
                "smoke_ok": smoke.get("ok"),
                "smoke_method": smoke.get("method"),
                "smoke_factors": smoke.get("factors"),
            },
            indent=2,
        ),
        flush=True,
    )
    if not smoke.get("ok"):
        return 1

    N = RSA100_N
    bl, B, B2 = _B_of(N)
    print(
        json.dumps({"target": "RSA-100", "bitlen": bl, "B": B, "B2": B2}, indent=2),
        flush=True,
    )
    got = fold_domain_factor(N)
    got = dict(got)
    got["wall"] = time.perf_counter() - t0
    got["pin"] = "D1D38A"
    got["B_raised"] = False
    got["factors_looked_up"] = False
    # do not persist factors of the smoke N as if they were RSA-100
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "domain_factor",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "B_raised": False,
        "factors_looked_up": False,
        "smoke_ok": True,
        "rsa100_ok": bool(got.get("ok")),
        "rsa100_method": got.get("method"),
        "rsa100_B": B,
        "rsa100_B2": B2,
        "rsa100_n_fermat_k": got.get("n_fermat_k"),
        "rsa100_n_curves": got.get("n_curves"),
        "rsa100_factors_bits": [
            int(f).bit_length() for f in (got.get("factors") or [])
        ],
        "wall_seconds": got["wall"],
        "note": got.get("note"),
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "domain_factor.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [
        "# Domain-fold factor — 35 pin D_eff on the RSA-100 miss",
        "",
        f"**{'hit' if report['rsa100_ok'] else 'miss'}** · pin D1D38A **not edited** · B **not raised** · factors **not looked up**",
        "",
        "Same move as \(V_{cb}\) / \(H_0\): change **domain / \(D_{\\mathrm{eff}}\)**, not a coefficient. "
        "Fermat \(k\) and ECM \(a\) are the 35 pin \(D_{\\mathrm{eff}}\) values (and pairwise products). "
        f"Locked B = `{B}`, B2 = `{B2}`. 60-bit smoke split via `{smoke.get('method')}`.",
        "",
        "RSA-100 is an artificial challenge modulus, not a pin observable. "
        "\(S(\\mathrm{QC})\) does not encode its factors. If this lane misses, "
        "that is the smoothness / Fermat-gap wall, not a reason to edit the pin.",
        "",
        f"| rsa100 | `{report['rsa100_method']}` | ok={report['rsa100_ok']} | "
        f"fermat_k={report['rsa100_n_fermat_k']} | ecm_curves={report['rsa100_n_curves']} |",
        "",
        "```powershell",
        "python -m fsot_quantum.fold_domain_factor",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "DOMAIN_FACTOR.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "DOMAIN_FACTOR.md").write_text(text, encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    return 0 if report["rsa100_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
