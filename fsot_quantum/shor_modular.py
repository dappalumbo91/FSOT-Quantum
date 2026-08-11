"""
Full modular-exponentiation path for tiny Shor on Hilbert register.

State: |x>_t |y>_L  with y in 0..2^L-1, N fitting in L bits.
Apply: |x>|y> → |x>| (a^x * y) mod N >  when y < N (and y=1 usually).

For N=15, L=4, t=4 → 8 qubits (256 amps) — full unitary sim.
Then IQFT on x and CF recover period.

Zero free parameters. Seed only for QFT angles (π).
"""

from __future__ import annotations

import math
from typing import Any

from fsot_quantum.hilbert import Statevector
from fsot_quantum.qft_shor import apply_iqft, apply_qft, _continued_fraction, _convergents_fixed


def _period(a: int, N: int) -> int:
    x = 1
    for p in range(1, N * N):
        x = (x * a) % N
        if x == 1:
            return p
    raise ValueError("no period")


def apply_modular_exp(sv: Statevector, a: int, N: int, t_bits: int, l_bits: int) -> None:
    """
    In-place: for each basis |x>|y>, map y → (a^x * y) % N if y < N else y.
    x is low t_bits, y is high l_bits (or reverse). Convention:
      index = x + (y << t_bits)  — x in LSBs
    """
    n = sv.n
    assert n == t_bits + l_bits
    dim = 1 << n
    out = [0j] * dim
    mask_x = (1 << t_bits) - 1
    for i in range(dim):
        x = i & mask_x
        y = i >> t_bits
        if 0 < y < N:
            y2 = (pow(a, x, N) * y) % N
        else:
            y2 = y
        j = x + (y2 << t_bits)
        out[j] += sv.amps[i]
    sv.amps = out
    sv.normalize()


def shor_full_modular(a: int, N: int, t_bits: int | None = None) -> dict[str, Any]:
    """
    1) Init |0>_t |1>_L
    2) H^⊗t on counting
    3) modular exp a^x mod N
    4) IQFT on counting
    5) measure mode + CF → r
    """
    L = max(1, math.ceil(math.log2(N + 1)))
    t = t_bits if t_bits is not None else 2 * L
    # cap for sim
    if t + L > 12:
        t = 12 - L
    n = t + L
    true_r = _period(a, N)

    sv = Statevector.zeros(n)
    # set y=1: index 1 << t
    sv = Statevector.basis(n, 1 << t)

    # H on all counting qubits
    for q in range(t):
        sv.H(q)

    apply_modular_exp(sv, a, N, t, L)

    # IQFT on counting register only — apply full IQFT by treating as subsystem
    # Easiest: bit-reorder — apply IQFT on first t qubits
    apply_iqft(sv, list(range(t)))

    probs = sv.probs()
    # marginal on counting: sum over y
    marg = [0.0] * (1 << t)
    for i, p in enumerate(probs):
        x = i & ((1 << t) - 1)
        marg[x] += p
    mode = max(range(len(marg)), key=lambda k: marg[k])

    def _period_candidates_from_phase(phase: int) -> list[int]:
        if phase == 0:
            return []
        x = phase / float(1 << t)
        cands: list[int] = []
        for _num, den in _convergents_fixed(_continued_fraction(x)):
            if den <= 0 or den > 2 * N:
                continue
            # all positive divisors of den that are valid periods
            d = 1
            while d * d <= den:
                if den % d == 0:
                    for r in (d, den // d):
                        if 0 < r <= N and pow(a, r, N) == 1:
                            cands.append(r)
                d += 1
        return cands

    candidates: list[int] = []
    for peak in sorted(range(len(marg)), key=lambda k: -marg[k])[:12]:
        candidates.extend(_period_candidates_from_phase(peak))
    # prefer smallest true period
    r_hat = min(candidates) if candidates else None

    return {
        "a": a,
        "N": N,
        "t_bits": t,
        "l_bits": L,
        "n_qubits": n,
        "true_period": true_r,
        "recovered_period": r_hat,
        "measure_mode": mode,
        "mode_prob": marg[mode],
        "ok": r_hat == true_r,
        "norm": sum(abs(z) ** 2 for z in sv.amps),
        "n_candidates": len(set(candidates)),
    }


def run_shor_modular_panel() -> dict[str, Any]:
    cases = [
        shor_full_modular(7, 15, t_bits=4),
        shor_full_modular(2, 15, t_bits=4),
        shor_full_modular(4, 15, t_bits=4),  # period 2
        shor_full_modular(5, 21, t_bits=5),
    ]
    # filter failures analysis
    n_ok = sum(1 for c in cases if c["ok"])
    report = {
        "panel": "shor_full_modular_exp",
        "cases": cases,
        "pass_count": n_ok,
        "total": len(cases),
        "overall_ok": n_ok == len(cases),
        "note": "Full Hilbert modular multiply + IQFT + CF; tiny N only",
    }
    return report
