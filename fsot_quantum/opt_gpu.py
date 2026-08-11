"""
GPU-batched Ising / MaxCut local search — many instances in parallel on CUDA.

Uses integer/float tensors; zero free params (seed multi-starts).
"""

from __future__ import annotations

import math
import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.domains import DOMAIN_SPIN_LAW, domain_scalar


def _t():
    import torch

    return torch


def _cycle_edges(n: int):
    return [(i, (i + 1) % n, 1) for i in range(n)]


def batch_maxcut_local(
    n: int,
    edges: list[tuple[int, int, int]],
    batch: int,
    *,
    maximize: bool = True,
) -> dict[str, Any]:
    """
    batch independent random-looking but seed-deterministic starts, polish on GPU.
    starts from φ-walk patterns per batch index.
    """
    torch = _t()
    dev = prefer_device()
    E = len(edges)
    # spins [B, n] as ±1 float for matmul-ish ops
    phi = float(SEEDS.phi)
    starts = []
    for b in range(batch):
        x = (b * int(phi * 1e6) + 2654435761) % (1 << max(n, 1))
        s = [1.0 if (x >> i) & 1 else -1.0 for i in range(n)]
        starts.append(s)
    # also domain-sign start
    base = 1.0 if domain_scalar(DOMAIN_SPIN_LAW) > 0 else -1.0
    starts[0] = [base] * n

    spins = torch.tensor(starts, dtype=torch.float64, device=dev)  # [B,n]
    ei = torch.tensor([e[0] for e in edges], device=dev, dtype=torch.long)
    ej = torch.tensor([e[1] for e in edges], device=dev, dtype=torch.long)
    # J = 1 for maxcut cut counting: cut = sum (1 - s_i s_j)/2

    def cut_vals(s):
        # s [B,n]
        prod = s[:, ei] * s[:, ej]
        return torch.sum((1.0 - prod) * 0.5, dim=-1)

    if dev == "cuda":
        torch.cuda.synchronize()
    t0 = time.perf_counter()

    # edge pass
    for _ in range(2):
        prod = spins[:, ei] * spins[:, ej]
        # if same sign (prod>0), flip j for that edge batch-wise — vectorized approx:
        # flip sites that participate in many uncut edges
        bad = (prod > 0).double()  # [B,E]
        # accumulate flip votes on vertices
        votes = torch.zeros(batch, n, device=dev, dtype=torch.float64)
        votes.scatter_add_(1, ej.unsqueeze(0).expand(batch, -1), bad)
        spins = torch.where(votes > 0, -spins, spins)

    # 1-flip coordinate ascent (few sweeps)
    sweeps = max(2, int(math.floor(float(SEEDS.pi))))
    for _ in range(sweeps):
        for i in range(n):
            # delta cut if flip i
            # neighbors of i
            # brute: flip, compare
            cur = cut_vals(spins)
            trial = spins.clone()
            trial[:, i] *= -1
            new = cut_vals(trial)
            better = new > cur
            spins = torch.where(better.unsqueeze(1), trial, spins)

    cuts = cut_vals(spins)
    if dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0

    return {
        "n": n,
        "batch": batch,
        "n_edges": E,
        "seconds": dt,
        "instances_per_sec": batch / dt if dt > 0 else None,
        "mean_cut": float(cuts.mean()),
        "max_cut": float(cuts.max()),
        "mean_ratio": float((cuts / E).mean()) if E else 0.0,
        "ok": True,
        "device": prefer_device(),
    }


def run_opt_gpu_panel() -> dict[str, Any]:
    rows = []
    for n, B in ((16, 512), (20, 256), (24, 128), (32, 64), (48, 32)):
        edges = _cycle_edges(n)
        # add seed chords
        phi = float(SEEDS.phi)
        x = 1
        for k in range(n // 2):
            x = (x * int(phi * 1e6) + k * 2654435761) % (n * n)
            a, b = x % n, (x // n) % n
            if a != b:
                if a > b:
                    a, b = b, a
                edges.append((a, b, 1))
        # dedupe
        edges = list({(a, b, 1) for a, b, _ in edges})
        try:
            rows.append({"job": f"maxcut_n{n}_B{B}", **batch_maxcut_local(n, edges, B)})
        except RuntimeError as e:
            rows.append({"job": f"maxcut_n{n}_B{B}", "ok": False, "error": str(e)})

    return {
        "panel": "opt_gpu",
        "instances": rows,
        "overall_ok": all(r.get("ok") for r in rows),
        "highlights": {
            "max_ips": max((r.get("instances_per_sec") or 0 for r in rows), default=0),
            "best_mean_ratio": max((r.get("mean_ratio") or 0 for r in rows), default=0),
        },
    }
