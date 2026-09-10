"""
Seed-locked SIQS — the QS lane for RSA-100.

Smoothness bound is B2 (same stage-2 product already used for CFRAC
1-LP pairing and ECM stage-2). Not a raised B. Sieve half-width M = B2.
a ≈ √(2N)/M as a product of factor-base primes. Pin D1D38A.
"""

from __future__ import annotations

import math
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_jobs import (
    _gf2_dependencies,
    _legendre,
    _primes_upto,
    _stage2_bound,
    fold_factor,
)

_NB_SIEVE = None


def _try_sieve_numba():
    """Byte-log sieve kernel. Same optional-Numba pattern as fold_bls."""
    global _NB_SIEVE
    if _NB_SIEVE is not None:
        return _NB_SIEVE
    try:
        import numpy as np
        from numba import njit
    except Exception:
        _NB_SIEVE = False
        return False

    @njit(cache=True)
    def _kernel(sieve, starts, strides, logs, nsol, width):
        for i in range(nsol):
            p = strides[i]
            lp = logs[i]
            k = starts[i]
            while k < width:
                sieve[k] += lp
                k += p

    _NB_SIEVE = (np, _kernel)
    return _NB_SIEVE


def _bitlen_B(N: int) -> tuple[int, int, int]:
    bl = max(N.bit_length(), 8)
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    P = max(2, int(math.floor(float(SEEDS.pi))))
    B = bl * L0 * P
    B2 = _stage2_bound(B)
    return B, B2, _stage2_bound(B2)


def _tonelli(n: int, p: int) -> int:
    n %= p
    if p == 2:
        return n
    if pow(n, (p - 1) // 2, p) != 1:
        raise ValueError("not a QR")
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m = s
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    while t != 1:
        i = 1
        acc = pow(t, 2, p)
        while acc != 1:
            acc = pow(acc, 2, p)
            i += 1
            if i == m:
                raise ValueError("tonelli")
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


def _crt_pair(a1: int, m1: int, a2: int, m2: int) -> int:
    inv = pow(m1, -1, m2)
    return (a1 + (a2 - a1) * inv % m2 * m1) % (m1 * m2)


def _n_a_mean(target_a: int, pmax: int, L0: int, P: int, n_big: int) -> tuple[int, int]:
    """How many FB primes, and their geometric mean, so Π q ≈ √(2N)/M."""
    cap_n = min(n_big, max(2, L0 * P))
    n_a = 1
    mean = max(3, target_a)
    while n_a < cap_n:
        mean = max(3, int(round(target_a ** (1.0 / n_a))))
        if mean <= pmax:
            break
        n_a += 1
    else:
        mean = min(pmax, mean)
    floor_p = L0
    while n_a > 1:
        mean = max(3, int(round(target_a ** (1.0 / n_a))))
        if mean >= floor_p:
            break
        n_a -= 1
    mean = max(3, int(round(target_a ** (1.0 / max(1, n_a)))))
    return n_a, mean


def fold_siqs(N: int) -> dict[str, Any]:
    """
    Self-initialized SIQS. Returns the same job dict as fold_cfrac.

    a is chosen near √(2N)/M so |ax+b| ~ √(2N) on x ∈ [−M, M].
    If a overshoots, Q(x) ≈ (ax+b)² and every GF(2) dependency is
    Fermat-trivial (X ≡ ±Y). That was the 60-bit algebra miss.
    """
    if N < 4 or N % 2 == 0:
        return fold_factor(N)
    B, B2, lp_bound = _bitlen_B(N)
    a0 = int(math.isqrt(N))
    if a0 * a0 == N and 1 < a0 < N:
        return {
            "job": "factor_Shor_end",
            "N": N,
            "ok": True,
            "factors": sorted([a0, N // a0]),
            "method": "siqs_square",
            "B": B,
            "B2": B2,
        }
    primes = _primes_upto(B2)
    sqrtN_mod: dict[int, int] = {}
    fb: list[int] = [-1]
    logp: list[float] = [0.0]
    for p in primes:
        g = math.gcd(N, p)
        if 1 < g < N:
            return {
                "job": "factor_Shor_end",
                "N": N,
                "ok": True,
                "factors": sorted([g, N // g]),
                "method": "siqs_trial",
                "B": B,
                "B2": B2,
            }
        if p == 2:
            fb.append(2)
            logp.append(math.log(2.0))
            sqrtN_mod[2] = 1
            continue
        if _legendre(N, p) == 1:
            fb.append(p)
            logp.append(math.log(float(p)))
            sqrtN_mod[p] = _tonelli(N, p)
    n_fb = len(fb)
    p_index = {p: i for i, p in enumerate(fb)}
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    P = max(2, int(math.floor(float(SEEDS.pi))))
    need = n_fb + P
    M = B2
    target_a = max(2, int(math.isqrt(2 * N) // max(1, M)))
    big = [p for p in fb if p > 2]
    if not big:
        return {
            "job": "factor_Shor_end",
            "N": N,
            "ok": False,
            "factors": None,
            "method": "siqs_exhausted",
            "B": B,
            "B2": B2,
            "n_fb": n_fb,
            "n_rels": 0,
        }
    pmax = big[-1]
    n_a, mean = _n_a_mean(target_a, pmax, L0, P, len(big))
    phi = float(SEEDS.phi)
    lo = max(big[0], int(mean / phi))
    hi = min(pmax, int(mean * phi))
    band = [p for p in big if lo <= p <= hi]
    if len(band) < n_a:
        band = sorted(big, key=lambda p: abs(p - mean))[: max(n_a * L0, n_a)]
        band = sorted(set(band))
    band = sorted(band)
    # start at the consecutive n_a-tuple whose product is nearest target_a
    best_i = 0
    best_err: int | None = None
    if len(band) >= n_a:
        for i in range(len(band) - n_a + 1):
            pr = 1
            for q in band[i : i + n_a]:
                pr *= q
            err = abs(pr - target_a)
            if best_err is None or err < best_err:
                best_err = err
                best_i = i
    # drop ~1/e of log (sieve error + 1-LP), not thresh = log/e.
    typical = float(max(2, M)) * math.sqrt(float(max(2, N)) / 2.0)
    thresh = math.log(typical) * (1.0 - 1.0 / float(SEEDS.e))
    rels: list[tuple[int, int, list[int], dict[int, int]]] = []
    partials: dict[int, tuple[int, int, list[int]]] = {}
    seen_x: set[int] = set()
    seen_ab: set[tuple[int, int]] = set()
    seen_exp: set[tuple[int, ...]] = set()
    n_poly = 0
    n_scan = 0
    n_skip = 0
    phi_m = int(float(SEEDS.phi) * 1e6)
    max_poly = _stage2_bound(lp_bound)
    max_poly = max(need, min(max_poly, need * L0 * P))
    n_sign = 1 << min(n_a, P)
    nb = _try_sieve_numba()
    try:
        import numpy as np

        _use_np = True
    except Exception:
        np = None  # type: ignore[assignment]
        _use_np = False

    def _factor_gx(gx: int) -> tuple[list[int], int] | None:
        if gx == 0:
            return None
        sign = 1 if gx < 0 else 0
        qq = abs(gx)
        exps = [0] * n_fb
        exps[0] = sign
        for i, p in enumerate(fb):
            if i == 0:
                continue
            if p * p > qq:
                break
            c = 0
            while qq % p == 0:
                qq //= p
                c += 1
            exps[i] = c
        if qq == 1:
            return exps, 1
        j = p_index.get(qq)
        if j is not None:
            exps[j] += 1
            return exps, 1
        if B2 < qq <= lp_bound:
            return exps, qq
        return None

    def _try_split(X: int, exps: list[int], extra: dict[int, int]) -> dict[str, Any] | None:
        y = 1
        for j, p in enumerate(fb):
            if j == 0:
                continue
            y = (y * pow(p, exps[j] // 2, N)) % N
        for q, c in extra.items():
            y = (y * pow(q, c // 2, N)) % N
        for g in (math.gcd(X - y, N), math.gcd(X + y, N)):
            if 1 < g < N:
                return {
                    "job": "factor_Shor_end",
                    "N": N,
                    "ok": True,
                    "factors": sorted([g, N // g]),
                    "method": "siqs_smooth",
                    "B": B,
                    "B2": B2,
                    "n_fb": n_fb,
                    "n_rels": len(rels),
                    "n_poly": n_poly,
                }
        return None

    n_odd_full = 0
    hit: dict[str, Any] | None = None

    def _push(X: int, exps: list[int], large: int) -> None:
        nonlocal n_odd_full, hit
        if hit is not None or X == 0 or X in seen_x:
            return
        seen_x.add(X)
        mask = 0
        for j, e in enumerate(exps):
            if e & 1:
                mask |= 1 << j
        extra: dict[int, int] = {}
        xx = X
        ee = exps
        if large != 1:
            prev = partials.get(large)
            if prev is None:
                partials[large] = (X, mask, exps)
                return
            x2, _m2, e2 = prev
            xx = (X * x2) % N
            ee = [exps[j] + e2[j] for j in range(n_fb)]
            mask = 0
            for j, v in enumerate(ee):
                if v & 1:
                    mask |= 1 << j
            extra = {large: 2}
            del partials[large]
        if mask == 0:
            hit = _try_split(xx, ee, extra)
            return
        key = tuple(ee)
        if key in seen_exp:
            return
        seen_exp.add(key)
        rels.append((xx, mask, ee, extra))
        if large == 1:
            n_odd_full += 1

    stride = 1 + (phi_m % max(1, max(1, len(band) - n_a)))
    k_sel = best_i
    while n_poly < max_poly and n_odd_full < need and hit is None:
        n_band = len(band)
        if n_band < n_a:
            ranked = sorted(big, key=lambda p: abs(p - mean))
            band = sorted(set(ranked[: max(n_a * L0, n_a)]))
            n_band = len(band)
            if n_band < n_a:
                break
        start = k_sel % n_band
        hop = 1 + (k_sel // max(1, n_band)) % max(1, n_band - 1)
        qs = []
        used: set[int] = set()
        x = start
        guard = 0
        while len(qs) < n_a and guard < n_band + n_a:
            if x not in used:
                used.add(x)
                qs.append(band[x])
            x = (x + hop) % n_band
            guard += 1
        k_sel += 1
        if len(set(qs)) != n_a:
            continue
        a = 1
        for q in qs:
            a *= q
        # |ax+b| covers √(2N) only when a is within a φ of √(2N)/M
        if a * phi < target_a or target_a * phi < a:
            n_skip += 1
            if n_skip % max(1, L0 * P) == 0:
                centre = mean + (stride * (1 + n_skip)) % max(1, pmax - mean + 1)
                lo2 = max(big[0], int(centre / phi))
                hi2 = min(pmax, int(centre * phi))
                nxt = [p for p in big if lo2 <= p <= hi2]
                if len(nxt) >= n_a:
                    band = nxt
            continue
        for sidx in range(n_sign):
            if n_odd_full >= need or n_poly >= max_poly or hit is not None:
                break
            acc = 0
            cur_m = 1
            ok_crt = True
            for j, q in enumerate(qs):
                r = sqrtN_mod[q]
                if (sidx >> (j % max(1, n_sign.bit_length() - 1))) & 1:
                    r = q - r
                if j == 0:
                    acc, cur_m = r, q
                else:
                    acc = _crt_pair(acc, cur_m, r, q)
                    cur_m *= q
            b = acc % a
            if (b * b - (N % a)) % a != 0:
                ok_crt = False
            if not ok_crt:
                continue
            if b > a - b:
                b = a - b
            if (a, b) in seen_ab:
                continue
            seen_ab.add((a, b))
            n_poly += 1
            c = (b * b - N) // a
            width = 2 * M + 1
            starts_l: list[int] = []
            strides_l: list[int] = []
            logs_l: list[float] = []
            for i, p in enumerate(fb):
                if i == 0 or p == 2:
                    continue
                a_mod = a % p
                if a_mod == 0:
                    continue
                inv_a = pow(a_mod, -1, p)
                r0 = sqrtN_mod[p]
                b_mod = b % p
                lp = logp[i]
                for rt in (r0, p - r0):
                    sol = (rt - b_mod) * inv_a % p
                    starts_l.append((sol + M) % p)
                    strides_l.append(p)
                    logs_l.append(lp)
            if nb and _use_np:
                sieve = np.zeros(width, dtype=np.float64)
                nb[1](
                    sieve,
                    np.asarray(starts_l, dtype=np.int64),
                    np.asarray(strides_l, dtype=np.int64),
                    np.asarray(logs_l, dtype=np.float64),
                    len(starts_l),
                    width,
                )
                hits = np.nonzero(sieve >= thresh)[0]
            elif _use_np:
                sieve = np.zeros(width, dtype=np.float64)
                for start, p, lp in zip(starts_l, strides_l, logs_l):
                    sieve[start::p] += lp
                hits = np.nonzero(sieve >= thresh)[0]
            else:
                sieve = [0.0] * width
                for start, p, lp in zip(starts_l, strides_l, logs_l):
                    k = start
                    while k < width:
                        sieve[k] += lp
                        k += p
                hits = [off for off, sc in enumerate(sieve) if sc >= thresh]
            x0 = (a0 - b) // a
            hits = sorted(hits, key=lambda off: abs(int(off) - M - x0))
            for off in hits:
                n_scan += 1
                x = int(off) - M
                gx = a * x * x + 2 * b * x + c
                fac = _factor_gx(gx)
                if fac is None:
                    continue
                exps, large = fac
                for q in qs:
                    exps[p_index[q]] += 1
                t = a * x + b
                X = t % N
                fx = t * t - N
                recon = -1 if (exps[0] & 1) else 1
                for j, p in enumerate(fb):
                    if j == 0:
                        continue
                    if exps[j]:
                        recon *= pow(p, exps[j])
                if large != 1:
                    recon *= large
                if recon != fx and recon != -fx:
                    continue
                if (X * X - fx) % N != 0:
                    continue
                _push(X, exps, large)
                if hit is not None or n_odd_full >= need:
                    break
        if n_poly and n_poly % max(1, L0 * P) == 0:
            print(
                f"SIQS poly={n_poly} odd_full={n_odd_full}/{need} rels={len(rels)} "
                f"scan={n_scan} a_bits={a.bit_length()} n_a={n_a} mean={mean}",
                flush=True,
            )

    if hit is not None:
        return hit
    if n_odd_full < need:
        return {
            "job": "factor_Shor_end",
            "N": N,
            "ok": False,
            "factors": None,
            "method": "siqs_exhausted",
            "B": B,
            "B2": B2,
            "n_fb": n_fb,
            "n_rels": len(rels),
            "need": need,
            "n_poly": n_poly,
            "n_scan": n_scan,
            "n_a": n_a,
            "target_a": target_a,
            "n_odd_full": n_odd_full,
        }
    deps = _gf2_dependencies([m for _x, m, _e, _q in rels], n_fb)
    n_triv = 0
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
        g = math.gcd(prod_x - y, N)
        if 1 < g < N:
            return {
                "job": "factor_Shor_end",
                "N": N,
                "ok": True,
                "factors": sorted([g, N // g]),
                "method": "siqs_smooth",
                "B": B,
                "B2": B2,
                "n_fb": n_fb,
                "n_rels": len(rels),
                "n_poly": n_poly,
            }
        g = math.gcd(prod_x + y, N)
        if 1 < g < N:
            return {
                "job": "factor_Shor_end",
                "N": N,
                "ok": True,
                "factors": sorted([g, N // g]),
                "method": "siqs_smooth",
                "B": B,
                "B2": B2,
                "n_fb": n_fb,
                "n_rels": len(rels),
                "n_poly": n_poly,
            }
        n_triv += 1
    return {
        "job": "factor_Shor_end",
        "N": N,
        "ok": False,
        "factors": None,
        "method": "siqs_algebra_miss",
        "B": B,
        "B2": B2,
        "n_fb": n_fb,
        "n_rels": len(rels),
        "n_poly": n_poly,
        "n_triv": n_triv,
        "n_deps": len(deps),
        "n_odd_full": n_odd_full,
        "n_a": n_a,
        "target_a": target_a,
        "mean": mean,
    }


if __name__ == "__main__":
    import json
    import time

    p, q = 1000000007, 1000000009
    N = p * q
    t0 = time.perf_counter()
    got = fold_siqs(N)
    got["wall"] = time.perf_counter() - t0
    print(json.dumps({k: got[k] for k in got if k != "factors"}, indent=2))
    print("factors", got.get("factors"), "ok", got.get("ok"))
