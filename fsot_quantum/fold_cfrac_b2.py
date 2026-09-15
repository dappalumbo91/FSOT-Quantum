"""
CFRAC at smoothness B2 — the unused pairing that is the RSA wall.

The wall is u = ln|Q| / ln(bound):
  - SIQS: |g| ~ 2^182, bound B2, u ≈ 10.4, expected smooth ≪ 1
  - CFRAC at B: |Q| ~ √N = 2^165, bound B, u ≈ 12.7, 0 rels
  - This lane: |Q| ~ √N, bound B2 (same stage-2 product SIQS already
    uses). Not a raised B. Pin D1D38A.

python -m fsot_quantum.fold_cfrac_b2
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
from fsot_quantum.fold_jobs import (
    _gf2_dependencies,
    _legendre,
    _primes_upto,
    _stage2_bound,
    fold_factor,
)
from fsot_quantum.rsa100 import RSA100_N


def _bitlen_B(N: int) -> tuple[int, int, int, int]:
    bl = max(N.bit_length(), 8)
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    P = max(2, int(math.floor(float(SEEDS.pi))))
    B = bl * L0 * P
    B2 = _stage2_bound(B)
    return bl, B, B2, _stage2_bound(B2)


def fold_cfrac_b2(N: int) -> dict[str, Any]:
    """
    Continued-fraction factor with FB = B2, 1-LP to stage-2(B2).
    Same CF walk as fold_cfrac. Smoothness is the SIQS bound, not B.
    """
    if N < 4 or N % 2 == 0:
        return fold_factor(N)
    bl, B, B2, lp_bound = _bitlen_B(N)
    a0 = int(math.isqrt(N))
    if a0 * a0 == N and 1 < a0 < N:
        return {
            "job": "factor_Shor_end",
            "N": N,
            "ok": True,
            "factors": sorted([a0, N // a0]),
            "method": "cfrac_b2_square",
            "B": B,
            "B2": B2,
        }
    primes = _primes_upto(B2)
    fb: list[int] = [-1]
    p_index: dict[int, int] = {}
    for p in primes:
        g = math.gcd(N, p)
        if 1 < g < N:
            return {
                "job": "factor_Shor_end",
                "N": N,
                "ok": True,
                "factors": sorted([g, N // g]),
                "method": "cfrac_b2_trial",
                "B": B,
                "B2": B2,
            }
        if p == 2:
            p_index[2] = len(fb)
            fb.append(2)
            continue
        if _legendre(N, p) == 1:
            p_index[p] = len(fb)
            fb.append(p)
    n_fb = len(fb)
    need = n_fb + max(2, int(math.floor(float(SEEDS.pi))))
    lp_primes = set(_primes_upto(lp_bound))
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    P = max(2, int(math.floor(float(SEEDS.pi))))
    cap = lp_bound
    ks = (
        1,
        2,
        max(2, int(math.floor(float(SEEDS.pi)))),
        max(2, int(math.floor(float(SEEDS.e)))),
        max(2, int(math.floor(float(SEEDS.phi)))),
    )

    def _sign_exp(n: int, Q: int) -> int:
        s = 1 if n & 1 else 0
        if Q < 0:
            s ^= 1
        return s

    last: dict[str, Any] | None = None
    seen_k: set[int] = set()
    for k in ks:
        if k in seen_k:
            continue
        seen_k.add(k)
        M = k * N
        a0k = int(math.isqrt(M))
        P_prev, Q_prev = 0, 1
        a = a0k
        A_prev2, A_prev1 = 1, a0k % N
        rels: list[tuple[int, int, list[int], dict[int, int]]] = []
        partials: dict[int, tuple[int, int, list[int]]] = {}
        steps = 0
        n_full = 0
        n_lp = 0
        seen_q: set[int] = set()
        for n in range(1, cap + 1):
            Pcur = a * Q_prev - P_prev
            if Q_prev == 0:
                break
            Q = (M - Pcur * Pcur) // Q_prev
            if Q == 0:
                break
            a = (a0k + Pcur) // Q
            A = (a * A_prev1 + A_prev2) % N
            steps += 1
            Q_abs = abs(Q)
            if Q_abs > 1 and Q_abs not in seen_q:
                seen_q.add(Q_abs)
                qq = Q_abs
                exps = [0] * n_fb
                exps[0] = _sign_exp(n, Q)
                mask = 1 if exps[0] & 1 else 0
                for i, p in enumerate(fb):
                    if i == 0:
                        continue
                    if p * p > qq:
                        break
                    c = 0
                    while qq % p == 0:
                        qq //= p
                        c += 1
                    if c:
                        exps[i] = c
                        if c & 1:
                            mask ^= 1 << i
                if qq == 1:
                    rels.append((A_prev1, mask, exps, {}))
                    n_full += 1
                else:
                    j = p_index.get(qq)
                    if j is not None:
                        exps[j] += 1
                        if exps[j] & 1:
                            mask ^= 1 << j
                        else:
                            mask &= ~(1 << j)
                        rels.append((A_prev1, mask, exps, {}))
                        n_full += 1
                    elif B2 < qq <= lp_bound and qq in lp_primes:
                        prev = partials.get(qq)
                        n_lp += 1
                        if prev is None:
                            partials[qq] = (A_prev1, mask, exps)
                        else:
                            x2, _m2, e2 = prev
                            xx = (A_prev1 * x2) % N
                            e = [exps[j] + e2[j] for j in range(n_fb)]
                            m = 0
                            for j, c in enumerate(e):
                                if c & 1:
                                    m |= 1 << j
                            rels.append((xx, m, e, {qq: 2}))
                            del partials[qq]
            A_prev2, A_prev1 = A_prev1, A
            P_prev, Q_prev = Pcur, Q
            if steps % max(1, L0 * P * B) == 0:
                print(
                    f"CFRAC-B2 k={k} steps={steps}/{cap} "
                    f"full={n_full} lp={n_lp} rels={len(rels)}/{need}",
                    flush=True,
                )
            if len(rels) >= need:
                break
        if len(rels) < need:
            last = {
                "job": "factor_Shor_end",
                "N": N,
                "ok": False,
                "factors": None,
                "method": "cfrac_b2_exhausted",
                "B": B,
                "B2": B2,
                "lp_bound": lp_bound,
                "k": k,
                "n_rels": len(rels),
                "n_full": n_full,
                "n_lp": n_lp,
                "need": need,
                "n_fb": n_fb,
                "steps": steps,
            }
            continue
        deps = _gf2_dependencies([m for _x, m, _e, _q in rels], n_fb)
        hit: dict[str, Any] | None = None
        for idxs in deps:
            prod_x = 1
            y = 1
            tot = [0] * n_fb
            extra: dict[int, int] = {}
            for i in idxs:
                x, _m, exps, exq = rels[i]
                prod_x = (prod_x * x) % N
                for j, e in enumerate(exps):
                    tot[j] += e
                for q, c in exq.items():
                    extra[q] = extra.get(q, 0) + c
            for j, p in enumerate(fb):
                if j == 0:
                    continue
                y = (y * pow(p, tot[j] // 2, N)) % N
            for q, c in extra.items():
                y = (y * pow(q, c // 2, N)) % N
            for g in (math.gcd(prod_x - y, N), math.gcd(prod_x + y, N)):
                if 1 < g < N:
                    hit = {
                        "job": "factor_Shor_end",
                        "N": N,
                        "ok": True,
                        "factors": sorted([g, N // g]),
                        "method": "cfrac_b2_smooth",
                        "B": B,
                        "B2": B2,
                        "lp_bound": lp_bound,
                        "k": k,
                        "n_rels": len(rels),
                        "n_fb": n_fb,
                        "steps": steps,
                    }
                    break
            if hit is not None:
                break
        if hit is not None:
            return hit
        last = {
            "job": "factor_Shor_end",
            "N": N,
            "ok": False,
            "factors": None,
            "method": "cfrac_b2_algebra_miss",
            "B": B,
            "B2": B2,
            "k": k,
            "n_rels": len(rels),
            "need": need,
            "n_fb": n_fb,
            "steps": steps,
        }
    return last if last is not None else {
        "job": "factor_Shor_end",
        "N": N,
        "ok": False,
        "factors": None,
        "method": "cfrac_b2_exhausted",
        "B": B,
        "B2": B2,
        "steps": 0,
    }


def main() -> int:
    t0 = time.perf_counter()
    smoke = fold_cfrac_b2(1000000007 * 1000000009)
    print(
        json.dumps(
            {
                "smoke_ok": smoke.get("ok"),
                "smoke_method": smoke.get("method"),
                "smoke_factors": smoke.get("factors"),
                "smoke_n_rels": smoke.get("n_rels"),
            },
            indent=2,
        ),
        flush=True,
    )
    if not smoke.get("ok"):
        return 1
    p, q = 9223372036854775837, 13000000000000000171
    t1 = time.perf_counter()
    bit64 = fold_cfrac_b2(p * q)
    print(
        json.dumps(
            {
                "bit64_ok": bit64.get("ok"),
                "bit64_method": bit64.get("method"),
                "bit64_factors_bits": [
                    int(f).bit_length() for f in (bit64.get("factors") or [])
                ],
                "bit64_n_rels": bit64.get("n_rels"),
                "bit64_wall": time.perf_counter() - t1,
            },
            indent=2,
        ),
        flush=True,
    )
    print(
        json.dumps({"target": "RSA-100", **dict(zip(
            ("bitlen", "B", "B2", "lp_bound"),
            _bitlen_B(RSA100_N),
        ))}, indent=2),
        flush=True,
    )
    got = fold_cfrac_b2(RSA100_N)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "cfrac_b2",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "B_raised": False,
        "factors_looked_up": False,
        "smoke_ok": True,
        "bit64_ok": bool(bit64.get("ok")),
        "rsa100_ok": bool(got.get("ok")),
        "rsa100_method": got.get("method"),
        "rsa100_B": got.get("B"),
        "rsa100_B2": got.get("B2"),
        "rsa100_n_rels": got.get("n_rels"),
        "rsa100_need": got.get("need"),
        "rsa100_n_fb": got.get("n_fb"),
        "rsa100_n_full": got.get("n_full"),
        "rsa100_n_lp": got.get("n_lp"),
        "rsa100_steps": got.get("steps"),
        "rsa100_k": got.get("k"),
        "rsa100_factors_bits": [
            int(f).bit_length() for f in (got.get("factors") or [])
        ],
        "wall_seconds": time.perf_counter() - t0,
        "wall": (
            "CFRAC |Q|~√N with smoothness B2 (SIQS bound). "
            "Not a raised B. The previous miss paired √N-Q with B, "
            "and ~N-Q with B2."
        ),
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "cfrac_b2.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [
        "# CFRAC-B2 — √N-sized Q at SIQS smoothness",
        "",
        f"**{'hit' if report['rsa100_ok'] else 'miss'}** · pin D1D38A **not edited** · B **not raised** · factors **not looked up**",
        "",
        "The RSA wall is \(u=\\ln|Q|/\\ln(\\mathrm{bound})\). SIQS sieved a "
        "~N-sized value at B2. Living CFRAC sieved a √N-sized value at B. "
        "This lane is the unused pairing: **√N-sized Q, bound B2** "
        "(same stage-2 product). Not a raised B.",
        "",
        f"60-bit smoke: `{smoke.get('method')}`. "
        f"64-bit RSA-shaped: `{bit64.get('method')}` ok={bit64.get('ok')}.",
        "",
        f"| rsa100 | `{report['rsa100_method']}` | rels "
        f"{report['rsa100_n_rels']}/{report['rsa100_need']} | "
        f"n_fb={report['rsa100_n_fb']} | steps={report['rsa100_steps']} | "
        f"k={report['rsa100_k']} |",
        "",
        "```powershell",
        "python -m fsot_quantum.fold_cfrac_b2",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "CFRAC_B2.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "CFRAC_B2.md").write_text(text, encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    return 0 if report["rsa100_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
