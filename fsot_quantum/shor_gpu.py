"""
GPU modular Shor for tiny N — full a^x mod N on batched / device statevector.

Uses torch complex128 on prefer_device(). Same math as shor_modular.py.
"""

from __future__ import annotations

import math
import time
from typing import Any

from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.hilbert_batch import BatchState
from fsot_quantum.qft_shor import _continued_fraction, _convergents_fixed
from fsot_lib.seeds import SEEDS


def _t():
    import torch

    return torch


def _period(a: int, N: int) -> int:
    x = 1
    for p in range(1, N * N):
        x = (x * a) % N
        if x == 1:
            return p
    raise ValueError("no period")


def apply_modular_exp_torch(amps, a: int, N: int, t_bits: int, l_bits: int):
    """amps: [dim] complex tensor → permutes basis by modular exp."""
    torch = _t()
    n = t_bits + l_bits
    dim = 1 << n
    mask_x = (1 << t_bits) - 1
    # build permutation index on CPU then to device (N tiny)
    perm = torch.empty(dim, dtype=torch.long)
    for i in range(dim):
        x = i & mask_x
        y = i >> t_bits
        if 0 < y < N:
            y2 = (pow(a, x, N) * y) % N
        else:
            y2 = y
        perm[i] = x + (y2 << t_bits)
    perm = perm.to(amps.device)
    out = torch.zeros_like(amps)
    out[perm] = amps
    # normalize
    nrm = torch.sqrt(torch.sum(torch.abs(out) ** 2))
    return out / nrm.clamp_min(1e-30)


def apply_qft_torch(amps, n: int, qubits: list[int]):
    """In-place style QFT on subset — work on [dim] vector via BatchState wrapper."""
    # Use BatchState with B=1
    bs = BatchState(n, 1, device=str(amps.device))
    bs.amps[0] = amps
    pi = float(SEEDS.pi)
    qs = qubits
    m = len(qs)
    for i in range(m):
        bs.H(qs[i])
        for j in range(i + 1, m):
            k = j - i
            bs.cphase(qs[j], qs[i], 2.0 * pi / (2**k))
    for i in range(m // 2):
        a, b = qs[i], qs[m - 1 - i]
        bs.CNOT(a, b)
        bs.CNOT(b, a)
        bs.CNOT(a, b)
    bs.normalize_()
    return bs.amps[0]


def apply_iqft_torch(amps, n: int, qubits: list[int]):
    bs = BatchState(n, 1, device=str(amps.device))
    bs.amps[0] = amps
    pi = float(SEEDS.pi)
    qs = qubits
    m = len(qs)
    for i in range(m // 2):
        a, b = qs[i], qs[m - 1 - i]
        bs.CNOT(a, b)
        bs.CNOT(b, a)
        bs.CNOT(a, b)
    for i in reversed(range(m)):
        for j in reversed(range(i + 1, m)):
            k = j - i
            bs.cphase(qs[j], qs[i], -2.0 * pi / (2**k))
        bs.H(qs[i])
    bs.normalize_()
    return bs.amps[0]


def shor_gpu(a: int, N: int, t_bits: int | None = None) -> dict[str, Any]:
    torch = _t()
    dev = prefer_device()
    L = max(1, math.ceil(math.log2(N + 1)))
    t = t_bits if t_bits is not None else min(2 * L, 12 - L)
    n = t + L
    true_r = _period(a, N)

    if dev == "cuda":
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
    t0 = time.perf_counter()

    dim = 1 << n
    amps = torch.zeros(dim, dtype=torch.complex128, device=dev)
    amps[1 << t] = 1.0 + 0j  # |0>_t |1>_L

    # H on counting
    bs = BatchState(n, 1, device=dev)
    bs.amps[0] = amps
    for q in range(t):
        bs.H(q)
    amps = bs.amps[0]

    amps = apply_modular_exp_torch(amps, a, N, t, L)
    amps = apply_iqft_torch(amps, n, list(range(t)))

    probs = (torch.abs(amps) ** 2).real
    # marginal x
    marg = torch.zeros(1 << t, dtype=torch.float64, device=dev)
    idx = torch.arange(dim, device=dev)
    x = idx & ((1 << t) - 1)
    marg.scatter_add_(0, x, probs)
    mode = int(torch.argmax(marg).item())
    mode_p = float(marg[mode])

    if dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0

    # CF recovery with divisor cleanup — more peaks for mid-size N
    candidates = []
    marg_cpu = marg.detach().cpu()
    top_k = min(1 << t, max(32, 2 * N))
    order = torch.argsort(marg_cpu, descending=True)[:top_k].tolist()
    for peak in order:
        if peak == 0:
            continue
        xf = peak / float(1 << t)
        for _num, den in _convergents_fixed(_continued_fraction(xf)):
            if den <= 0 or den > 2 * N:
                continue
            d = 1
            while d * d <= den:
                if den % d == 0:
                    for r in (d, den // d):
                        if 0 < r <= N and pow(a, r, N) == 1:
                            candidates.append(r)
                d += 1
    r_hat = min(candidates) if candidates else None
    mem = torch.cuda.max_memory_allocated() / (1024**2) if dev == "cuda" else None

    return {
        "a": a,
        "N": N,
        "n_qubits": n,
        "t_bits": t,
        "true_period": true_r,
        "recovered_period": r_hat,
        "ok": r_hat == true_r,
        "seconds": dt,
        "mode": mode,
        "mode_prob": mode_p,
        "peak_mem_mb": mem,
        "device": dev,
    }


def run_shor_gpu_panel() -> dict[str, Any]:
    """
    Tiny + mid ladder. Counting bits t grow with N so CF recovers period.
    n = t + L; mid cases ~14–16 qubits on consumer CUDA.
    """
    cases = [
        shor_gpu(7, 15, t_bits=4),
        shor_gpu(2, 15, t_bits=4),
        shor_gpu(4, 15, t_bits=4),
        shor_gpu(5, 21, t_bits=5),
        # climb: larger composite N (still classical-period verifiable)
        shor_gpu(2, 33, t_bits=8),   # 33=3*11, L=6, n=14
        shor_gpu(2, 35, t_bits=8),   # 35=5*7, n=14
        shor_gpu(2, 39, t_bits=8),   # 39=3*13, n=14
        shor_gpu(8, 51, t_bits=10),  # 51=3*17, L=6, n=16
    ]
    return {
        "panel": "shor_gpu",
        "cases": cases,
        "pass_count": sum(1 for c in cases if c["ok"]),
        "total": len(cases),
        "overall_ok": all(c["ok"] for c in cases),
        "note": "Full modular-exp statevector on GPU; not cryptographically large N",
    }
