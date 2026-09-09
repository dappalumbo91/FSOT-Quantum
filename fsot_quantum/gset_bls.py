"""
Seed-locked Breakout Local Search for MaxCut.

1-flip steepest descent plus adaptive perturbation (directed / swap /
random), tabu tenure from φ-hash in [⌊π⌋, n/⌊eπ⌋]. Jump L0 = ⌊eπ⌋.
Not a new coefficient — same two seed floors as B and ridge kicks.

Keep-if-better. Pin D1D38A.
"""

from __future__ import annotations

import math
from fsot_lib.seeds import SEEDS


def fold_bls(
    n: int,
    adj: list[list[int]],
    s0: list[int],
    cut0: int,
    *,
    budget: int | None = None,
) -> tuple[int, list[int]]:
    """
    BLS from a living 1-opt. Returns (cut, spins), never worse than cut0.
    """
    L0 = max(2, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    T = n
    P0 = 1.0 / float(SEEDS.phi)
    Q = 1.0 / float(SEEDS.e)
    ten_lo = max(2, int(math.floor(float(SEEDS.pi))))
    ten_hi = max(ten_lo + 1, n // L0)
    phi_m = int(float(SEEDS.phi) * 1e6)
    if budget is None:
        budget = n * n * L0

    def _hash32(x: int) -> int:
        return (phi_m * x + 2654435761) & 0xFFFFFFFF

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
        sig = tuple(s if s[0] == 1 else [-x for x in s])
        if omega > T:
            omega = 0
            kind = "B"
        elif sig == Cp:
            L += 1
            kind = "dir"
        else:
            L = L0
            kind = "dir"
        Cp = sig
        if omega == 0 and kind == "B":
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
