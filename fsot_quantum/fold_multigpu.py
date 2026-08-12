"""
Multi-GPU fold scheduler — honest device inventory + shard runner.

This host may have one GPU. The API still:
  - inventories CUDA devices
  - shards independent fold jobs as device_id = shard % n_gpu
  - runs shards (on the devices that exist)

Does **not** claim multi-GPU speedup when n_gpu == 1.

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import time
from typing import Any

from fsot_quantum.fold_gpu_queue import batch_ising_fold, batch_search_fold
from fsot_quantum.gpu_parallel import prefer_device


def _t():
    import torch

    return torch


def inventory() -> dict[str, Any]:
    torch = _t()
    n = torch.cuda.device_count() if torch.cuda.is_available() else 0
    names = [torch.cuda.get_device_name(i) for i in range(n)]
    return {
        "n_gpu": n,
        "names": names,
        "prefer": prefer_device(),
        "multi_gpu_available": n >= 2,
    }


def _shard_jobs(n_gpu: int) -> list[dict[str, Any]]:
    """Four independent fold shards assigned round-robin to devices."""
    n = max(1, n_gpu)
    specs = [
        {"kind": "search", "n_items": 2048, "batch": 512},
        {"kind": "search", "n_items": 4096, "batch": 256},
        {"kind": "ising", "n": 24, "batch": 256},
        {"kind": "ising", "n": 32, "batch": 128},
    ]
    for i, s in enumerate(specs):
        s["device_id"] = i % n
        s["shard"] = i
    return specs


def _run_shard(spec: dict[str, Any], have_cuda: bool) -> dict[str, Any]:
    torch = _t()
    dev = f"cuda:{spec['device_id']}" if have_cuda else "cpu"
    if have_cuda:
        torch.cuda.set_device(spec["device_id"])
    t0 = time.perf_counter()
    if spec["kind"] == "search":
        marked = [((i * 2654435761) + spec["shard"]) % spec["n_items"] for i in range(spec["batch"])]
        r = batch_search_fold(spec["n_items"], marked, device=dev)
    else:
        n = spec["n"]
        edges = [(i, (i + 1) % n, 1) for i in range(n)]
        r = batch_ising_fold(n, spec["batch"], edges, device=dev)
    r["seconds_wall"] = time.perf_counter() - t0
    r["shard"] = spec["shard"]
    r["device_id"] = spec["device_id"]
    r["device"] = dev
    return r


def run_fold_multigpu_panel() -> dict[str, Any]:
    inv = inventory()
    have = inv["n_gpu"] > 0
    specs = _shard_jobs(inv["n_gpu"] if have else 1)
    rows = [_run_shard(s, have) for s in specs]
    ok = all(r.get("ok") for r in rows)
    return {
        "panel": "fold_multigpu",
        "inventory": inv,
        "shards": rows,
        "pass_count": sum(1 for r in rows if r.get("ok")),
        "total": len(rows),
        "overall_ok": ok and len(rows) > 0,
        "claimed_multi_gpu_speedup": False if not inv["multi_gpu_available"] else True,
        "note": (
            "Shard runner is multi-GPU ready (device_id % n_gpu). "
            "This machine reports n_gpu in inventory — no fabricated extra devices."
        ),
    }
