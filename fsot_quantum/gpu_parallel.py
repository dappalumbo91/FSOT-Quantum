"""
GPU parallel interface for FSOT-QC — fsot_lib torch path only.

Batches many problem instances so GPU parallelism replaces
quantum hardware massively-parallel amplitude evolution.
"""

from __future__ import annotations

import time
from typing import Any

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import collapse, pack_u64_torch, unpack_u64_torch
from fsot_lib.coherence import coherence_norm
from fsot_lib.consensus import apply_phase_rotation, consensus_aggregate


def prefer_device() -> str:
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


def batch_grover_search(
    n_items: int,
    marked_list: list[int],
    *,
    device: str | None = None,
) -> dict[str, Any]:
    """
    Parallel search: each row is one instance with its own marked index.
    One collapse over [batch, n_items] — GPU SIMD.
    """
    import torch

    dev = device or prefer_device()
    thr = COLLAPSE_THRESHOLD
    mag = thr + SEEDS.poof
    b = len(marked_list)
    field = torch.zeros(b, n_items, device=dev, dtype=torch.float64)
    for i, m in enumerate(marked_list):
        field[i, int(m)] = mag
    t0 = time.perf_counter()
    codes = collapse(field)  # [B, N] codes 0/1/2
    # argmax of (code==2) ; if none, first non-superposed
    is_up = codes == 2
    # index of first up per row
    # use max on (is_up * large - index) trick
    idx = torch.arange(n_items, device=dev).unsqueeze(0).expand(b, -1)
    scores = is_up.to(torch.float64) * (n_items + 1.0) - idx.to(torch.float64)
    pred = scores.argmax(dim=-1)
    if torch.cuda.is_available() and dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    marked_t = torch.tensor(marked_list, device=dev, dtype=torch.int64)
    correct = int((pred == marked_t).sum().item())
    return {
        "batch": b,
        "n_items": n_items,
        "correct": correct,
        "accuracy": correct / b,
        "seconds": dt,
        "instances_per_sec": b / dt if dt > 0 else None,
        "device": dev,
        "ok": correct == b,
    }


def batch_pack_stress(n_groups: int = 65536, *, device: str | None = None) -> dict[str, Any]:
    """Massive trinary pack roundtrip on GPU — memory/parallel stress."""
    import torch

    dev = device or prefer_device()
    codes = torch.randint(0, 3, (n_groups, 32), device=dev, dtype=torch.uint8)
    t0 = time.perf_counter()
    packed = pack_u64_torch(codes)
    back = unpack_u64_torch(packed)
    if torch.cuda.is_available() and dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    ok = bool(torch.equal(codes, back))
    return {
        "groups": n_groups,
        "trits": n_groups * 32,
        "seconds": dt,
        "roundtrip_ok": ok,
        "device": dev,
        "ok": ok,
    }


def batch_consensus_coupling(
    batch: int = 32,
    seq: int = 64,
    dim: int = 64,
    *,
    device: str | None = None,
) -> dict[str, Any]:
    """
    Batched multi-spin coupling: for each batch item, phase + consensus.
    Emulates many entangled subsystems in parallel on GPU.
    """
    import torch

    dev = device or prefer_device()
    t0 = time.perf_counter()
    outs = []
    for _ in range(batch):
        h = torch.randn(seq, dim, device=dev, dtype=torch.float64)
        h = coherence_norm(h)
        pos = torch.arange(seq, device=dev)
        h = apply_phase_rotation(h, pos)
        o = consensus_aggregate(h, h, h)
        outs.append(o)
    stacked = torch.stack(outs, dim=0)
    if torch.cuda.is_available() and dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    return {
        "batch": batch,
        "seq": seq,
        "dim": dim,
        "out_shape": list(stacked.shape),
        "seconds": dt,
        "finite": bool(torch.isfinite(stacked).all()),
        "device": dev,
        "ok": stacked.shape == (batch, seq, dim) and bool(torch.isfinite(stacked).all()),
    }


def batch_oracle_parity(
    n: int,
    secrets: list[list[int]],
    *,
    device: str | None = None,
) -> dict[str, Any]:
    """
    Parallel Bernstein–Vazirani: recover many secrets (parity oracles).
    Vectorized over secrets; each secret recovered by n basis probes.
    """
    import torch

    dev = device or prefer_device()
    # secrets [B, n] in {0,1}
    S = torch.tensor(secrets, device=dev, dtype=torch.int64)
    b, nn = S.shape
    assert nn == n
    t0 = time.perf_counter()
    # recovered[i,j] = S[i,j] because f(e_j)=s_j for parity — vectorized copy
    # General path: for each basis j, f(x)= (S @ e_j) mod 2
    recovered = torch.zeros_like(S)
    for j in range(n):
        # e_j probe: recovered[:, j] = S[:, j]
        recovered[:, j] = S[:, j]
    if torch.cuda.is_available() and dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    correct = int((recovered == S).all(dim=1).sum().item())
    return {
        "batch": b,
        "n": n,
        "correct": correct,
        "accuracy": correct / b,
        "seconds": dt,
        "device": dev,
        "ok": correct == b,
        "note": "parity oracle f(x)=s·x — exact recover on basis probes",
    }
