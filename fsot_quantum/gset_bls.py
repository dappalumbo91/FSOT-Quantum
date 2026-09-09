"""
Seed-locked Breakout Local Search for MaxCut.

1-flip steepest descent plus adaptive perturbation (directed / swap /
random), tabu tenure from φ-hash in [⌊π⌋, n/⌊eπ⌋]. Jump L0 = ⌊eπ⌋.
Not a new coefficient — same two seed floors as B and ridge kicks.

seed_k offsets the φ-hash (0 = living trajectory). Paper-scale budget
is n²⌊eπ⌋⌊π³⌋, the seed analog of BLS 200000|V|.

Keep-if-better. Pin D1D38A.
"""

from __future__ import annotations

import math
from fsot_lib.seeds import SEEDS

_NB = None


def _l0() -> int:
    return max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))


def paper_budget(n: int) -> int:
    """n²⌊eπ⌋⌊π³⌋ — seed-locked analog of BLS 200000|V|."""
    pi3 = max(1, int(math.floor(float(SEEDS.pi) ** 3)))
    return n * n * _l0() * pi3


def _csr(adj: list[list[int]]):
    n = len(adj)
    total = 0
    for nbr in adj:
        total += len(nbr)
    offsets = [0] * (n + 1)
    neigh = [0] * total
    k = 0
    for i, nbr in enumerate(adj):
        offsets[i] = k
        for j in nbr:
            neigh[k] = j
            k += 1
    offsets[n] = k
    return offsets, neigh


def _try_numba():
    global _NB
    if _NB is not None:
        return _NB
    try:
        import numpy as np
        from numba import njit
    except Exception:
        _NB = False
        return False

    @njit(cache=True)
    def _hash32(phi_m, seed_k, x):
        return (phi_m * (x + seed_k) + 2654435761) & 0xFFFFFFFF

    @njit(cache=True)
    def _kernel(
        n,
        offsets,
        neigh,
        s,
        g,
        H,
        cp,
        best,
        c,
        best_c,
        budget,
        seed_k,
        L0,
        T,
        P0,
        Q,
        ten_lo,
        ten_hi,
        phi_m,
        target,
        strong,
    ):
        Iter = 0
        omega = 0
        L = L0
        last_rep = 0
        ten_span = ten_hi - ten_lo + 1
        s0 = s[0]
        for i in range(n):
            cp[i] = s[i] * s0
        while Iter < budget:
            while True:
                vm = -1
                bg = -1000000000
                for i in range(n):
                    if g[i] > bg:
                        bg = g[i]
                        vm = i
                if bg <= 0:
                    break
                s[vm] = -s[vm]
                c += g[vm]
                g[vm] = -g[vm]
                si = s[vm]
                a = offsets[vm]
                b = offsets[vm + 1]
                for k in range(a, b):
                    j = neigh[k]
                    if s[j] == si:
                        g[j] += 2
                    else:
                        g[j] -= 2
                H[vm] = Iter + ten_lo + (_hash32(phi_m, seed_k, Iter + vm) % ten_span)
                Iter += 1
                if Iter >= budget:
                    break
            if c > best_c:
                best_c = c
                for i in range(n):
                    best[i] = s[i]
                omega = 0
                if best_c >= target:
                    return best_c, Iter
            else:
                omega += 1
            same = True
            s0 = s[0]
            for i in range(n):
                if s[i] * s0 != cp[i]:
                    same = False
                    break
            if omega > T:
                omega = 0
                kind_b = True
                # Paper prose: distant-region jump. Tenure-high n/⌊eπ⌋.
                # Off for the φ-panel (that panel's job is the 3044 basin).
                if strong != 0:
                    L = max(L, n // L0)
            elif same:
                L += 1
                kind_b = False
            else:
                L = L0
                kind_b = False
            s0 = s[0]
            for i in range(n):
                cp[i] = s[i] * s0
            # Paper Alg. 2: ω=0 (just improved, or T stagnant) → random B.
            if omega == 0:
                ptype = 0
            else:
                pw = math.exp(-omega / max(1, T))
                P = pw if pw > P0 else P0
                u = (_hash32(phi_m, seed_k, Iter * 3 + 1) % 10000) / 10000.0
                if u < P * Q:
                    ptype = 1
                elif u < P:
                    ptype = 2
                else:
                    ptype = 0
            step = 0
            while step < L and Iter < budget:
                if ptype == 0:
                    v = _hash32(phi_m, seed_k, Iter * 7 + 13) % n
                elif ptype == 1:
                    vm = -1
                    bg = -1000000000
                    for i in range(n):
                        allowed = H[i] <= Iter or (c + g[i] > best_c)
                        if not allowed:
                            continue
                        if g[i] > bg:
                            bg = g[i]
                            vm = i
                    v = vm if vm >= 0 else (_hash32(phi_m, seed_k, Iter) % n)
                else:
                    v1 = -1
                    b1 = -1000000000
                    v2 = -1
                    b2 = -1000000000
                    for i in range(n):
                        allowed = H[i] <= Iter or (c + g[i] > best_c)
                        if not allowed:
                            continue
                        if s[i] == 1:
                            if g[i] > b1:
                                b1 = g[i]
                                v1 = i
                        else:
                            if g[i] > b2:
                                b2 = g[i]
                                v2 = i
                    if v1 >= 0:
                        s[v1] = -s[v1]
                        c += g[v1]
                        g[v1] = -g[v1]
                        si = s[v1]
                        a = offsets[v1]
                        b = offsets[v1 + 1]
                        for k in range(a, b):
                            j = neigh[k]
                            if s[j] == si:
                                g[j] += 2
                            else:
                                g[j] -= 2
                        H[v1] = Iter + ten_lo + (
                            _hash32(phi_m, seed_k, Iter + v1) % ten_span
                        )
                        Iter += 1
                        if Iter >= budget:
                            break
                    v = v2 if v2 >= 0 else (_hash32(phi_m, seed_k, Iter) % n)
                s[v] = -s[v]
                c += g[v]
                g[v] = -g[v]
                si = s[v]
                a = offsets[v]
                b = offsets[v + 1]
                for k in range(a, b):
                    j = neigh[k]
                    if s[j] == si:
                        g[j] += 2
                    else:
                        g[j] -= 2
                H[v] = Iter + ten_lo + (_hash32(phi_m, seed_k, Iter + v) % ten_span)
                Iter += 1
                step += 1
            if Iter - last_rep >= 5000000:
                last_rep = Iter
        return best_c, Iter

    _NB = (np, _kernel)
    return _NB


def fold_bls(
    n: int,
    adj: list[list[int]],
    s0: list[int],
    cut0: int,
    *,
    budget: int | None = None,
    seed_k: int = 0,
    target: int | None = None,
    use_numba: bool | None = None,
    strong_stagnation: bool = True,
) -> tuple[int, list[int]]:
    """
    BLS from a living 1-opt. Returns (cut, spins), never worse than cut0.
    seed_k=0 is the living trajectory. target early-stops (hunt).
    """
    L0 = _l0()
    T = n
    P0 = 1.0 / float(SEEDS.phi)
    Q = 1.0 / float(SEEDS.e)
    ten_lo = max(2, int(math.floor(float(SEEDS.pi))))
    ten_hi = max(ten_lo + 1, n // L0)
    phi_m = int(float(SEEDS.phi) * 1e6)
    if budget is None:
        budget = n * n * L0
    if target is None:
        target = 10 ** 18

    nb = _try_numba() if use_numba is not False else False
    if nb:
        np, kernel = nb
        offsets, neigh = _csr(adj)
        s = np.array(s0, dtype=np.int32)
        g = np.zeros(n, dtype=np.int32)
        for i, nbr in enumerate(adj):
            same = 0
            for j in nbr:
                if s[j] == s[i]:
                    same += 1
            g[i] = 2 * same - len(nbr)
        H = np.zeros(n, dtype=np.int64)
        cp = np.zeros(n, dtype=np.int32)
        best = s.copy()
        best_c, _it = kernel(
            n,
            np.array(offsets, dtype=np.int32),
            np.array(neigh, dtype=np.int32),
            s,
            g,
            H,
            cp,
            best,
            int(cut0),
            int(cut0),
            int(budget),
            int(seed_k),
            int(L0),
            int(T),
            float(P0),
            float(Q),
            int(ten_lo),
            int(ten_hi),
            int(phi_m),
            int(target),
            1 if strong_stagnation else 0,
        )
        return int(best_c), [int(x) for x in best]

    def _hash32(x: int) -> int:
        return (phi_m * (x + seed_k) + 2654435761) & 0xFFFFFFFF

    s = list(s0)
    g = [0] * n
    for i, nbr in enumerate(adj):
        same = 0
        for j in nbr:
            if s[j] == s[i]:
                same += 1
        g[i] = 2 * same - len(nbr)
    c = cut0
    best_c = cut0
    best = list(s)

    def _flip(v: int) -> None:
        nonlocal c
        s[v] = -s[v]
        c += g[v]
        g[v] = -g[v]
        si = s[v]
        for j in adj[v]:
            if s[j] == si:
                g[j] += 2
            else:
                g[j] -= 2

    H = [0] * n
    Iter = 0
    omega = 0
    L = L0
    Cp = tuple(s if s[0] == 1 else [-x for x in s])
    while Iter < budget:
        while True:
            vm = -1
            bg = -10**9
            for i in range(n):
                if g[i] > bg:
                    bg = g[i]
                    vm = i
            if bg <= 0:
                break
            _flip(vm)
            H[vm] = Iter + ten_lo + (_hash32(Iter + vm) % (ten_hi - ten_lo + 1))
            Iter += 1
            if Iter >= budget:
                break
        if c > best_c:
            best_c = c
            best = list(s)
            omega = 0
        else:
            omega += 1
        if best_c >= target:
            return best_c, best
        sig = tuple(s if s[0] == 1 else [-x for x in s])
        if omega > T:
            omega = 0
            kind = "B"
            if strong_stagnation:
                L = max(L, n // L0)
        elif sig == Cp:
            L += 1
            kind = "dir"
        else:
            L = L0
            kind = "dir"
        Cp = sig
        # Paper Alg. 2: ω=0 (just improved, or T stagnant) → random B.
        if omega == 0:
            ptype = "B"
        else:
            pw = math.exp(-omega / max(1, T))
            P = pw if pw > P0 else P0
            u = (_hash32(Iter * 3 + 1) % 10000) / 10000.0
            if u < P * Q:
                ptype = "A1"
            elif u < P:
                ptype = "A2"
            else:
                ptype = "B"
        for _ in range(L):
            if ptype == "B":
                v = _hash32(Iter * 7 + 13) % n
            elif ptype == "A1":
                vm = -1
                bg = -10**9
                for i in range(n):
                    allowed = H[i] <= Iter or (c + g[i] > best_c)
                    if not allowed:
                        continue
                    if g[i] > bg:
                        bg = g[i]
                        vm = i
                v = vm if vm >= 0 else (_hash32(Iter) % n)
            else:
                v1 = -1
                b1 = -10**9
                v2 = -1
                b2 = -10**9
                for i in range(n):
                    allowed = H[i] <= Iter or (c + g[i] > best_c)
                    if not allowed:
                        continue
                    if s[i] == 1:
                        if g[i] > b1:
                            b1 = g[i]
                            v1 = i
                    else:
                        if g[i] > b2:
                            b2 = g[i]
                            v2 = i
                if v1 >= 0:
                    _flip(v1)
                    H[v1] = Iter + ten_lo + (
                        _hash32(Iter + v1) % (ten_hi - ten_lo + 1)
                    )
                    Iter += 1
                v = v2 if v2 >= 0 else (_hash32(Iter) % n)
            _flip(v)
            H[v] = Iter + ten_lo + (_hash32(Iter + v) % (ten_hi - ten_lo + 1))
            Iter += 1
            if Iter >= budget:
                break
    return best_c, best
