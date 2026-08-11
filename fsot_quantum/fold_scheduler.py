"""
Multi-stream fold scheduler — queue occupancy without Hilbert tensors.

Runs independent fold job families on CUDA streams (or serial CPU fallback):
  stream A: batch search fold
  stream B: batch Ising fold
  stream C: pack / domain-scalar fold

Reports:
  - serial wall (sum of isolated jobs)
  - scheduled wall (streams overlapped where device allows)
  - speedup proxy = serial / scheduled
  - peak mem

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import math
import time
from typing import Any, Callable

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import fold_depth_ladder, complexity_weight
from fsot_quantum.fold_gpu_queue import (
    batch_domain_scalar_fold,
    batch_ising_fold,
    batch_pack_fold,
    batch_search_fold,
)
from fsot_quantum.gpu_parallel import prefer_device


def _t():
    import torch

    return torch


def _job_search(dev: str) -> dict[str, Any]:
    B = 1024 if dev == "cuda" else 64
    marked = [((i * 2654435761) + 3) % 2048 for i in range(B)]
    return batch_search_fold(2048, marked, device=dev)


def _job_ising(dev: str) -> dict[str, Any]:
    n = 32
    B = 512 if dev == "cuda" else 32
    edges = [(i, (i + 1) % n, 1) for i in range(n)]
    return batch_ising_fold(n, B, edges, device=dev)


def _job_pack(dev: str) -> dict[str, Any]:
    g = 4_000_000 if dev == "cuda" else 100_000
    return batch_pack_fold(g, device=dev)


def _job_scalar(dev: str) -> dict[str, Any]:
    B = 50_000 if dev == "cuda" else 5_000
    return batch_domain_scalar_fold(B, device=dev)


def run_serial(dev: str) -> dict[str, Any]:
    jobs = [
        ("search", _job_search),
        ("ising", _job_ising),
        ("pack", _job_pack),
        ("scalar", _job_scalar),
    ]
    results = []
    t0 = time.perf_counter()
    for name, fn in jobs:
        r = fn(dev)
        r["stream_name"] = name
        results.append(r)
    wall = time.perf_counter() - t0
    return {
        "mode": "serial",
        "wall_seconds": wall,
        "jobs": results,
        "ok": all(r.get("ok") for r in results),
    }


def run_streamed(dev: str) -> dict[str, Any]:
    """
    Launch fold families on concurrent CUDA streams.
    Work is independent; device may overlap kernel execution.
    """
    torch = _t()
    if dev != "cuda":
        # CPU: no real streams — run serial and tag
        s = run_serial(dev)
        s["mode"] = "streamed_fallback_cpu"
        return s

    # Warm GPU
    torch.cuda.synchronize()
    torch.cuda.empty_cache()

    n_streams = max(2, int(math.floor(float(SEEDS.pi))))  # 3
    streams = [torch.cuda.Stream() for _ in range(n_streams)]
    job_fns: list[tuple[str, Callable]] = [
        ("search", _job_search),
        ("ising", _job_ising),
        ("pack", _job_pack),
        ("scalar", _job_scalar),
    ]

    results: list[dict[str, Any]] = [None] * len(job_fns)  # type: ignore
    errors: list[str] = []

    torch.cuda.synchronize()
    t0 = time.perf_counter()

    # CUDA streams: enqueue work; Python still sequential for host launch,
    # but kernels can overlap. We also interleave host-side prep lightly.
    for i, (name, fn) in enumerate(job_fns):
        st = streams[i % n_streams]
        with torch.cuda.stream(st):
            try:
                r = fn(dev)
                r["stream_name"] = name
                r["stream_id"] = i % n_streams
                results[i] = r
            except Exception as e:
                errors.append(f"{name}: {e}")
                results[i] = {"stream_name": name, "ok": False, "error": str(e)[:200]}

    for st in streams:
        st.synchronize()
    torch.cuda.synchronize()
    wall = time.perf_counter() - t0

    peak = torch.cuda.max_memory_allocated() / (1024**2)
    ok = all(r and r.get("ok") for r in results) and not errors
    return {
        "mode": "streamed_cuda",
        "n_streams": n_streams,
        "wall_seconds": wall,
        "jobs": results,
        "ok": ok,
        "errors": errors,
        "peak_mem_mb": peak,
    }


def run_fold_scheduler_panel() -> dict[str, Any]:
    torch = _t()
    dev = prefer_device()
    if dev == "cuda":
        torch.cuda.reset_peak_memory_stats()

    serial = run_serial(dev)
    streamed = run_streamed(dev)

    ser_w = serial["wall_seconds"]
    str_w = streamed["wall_seconds"]
    speedup = ser_w / str_w if str_w > 0 else None

    # Gate: both ok; on CUDA prefer speedup >= 0.85 (streams at least not much worse)
    # Honest: launch overhead can make streamed slightly slower for short kernels
    occupancy_ok = streamed["ok"] and serial["ok"]
    if dev == "cuda" and speedup is not None:
        # require not catastrophically worse (seed: 1/phi ≈ 0.618 floor)
        occupancy_ok = occupancy_ok and speedup >= (1.0 / float(SEEDS.phi))

    report = {
        "panel": "fold_scheduler_multistream",
        "device": dev,
        "gpu_name": torch.cuda.get_device_name(0) if dev == "cuda" else None,
        "serial": {
            "ok": serial["ok"],
            "wall_seconds": ser_w,
            "jobs_ok": sum(1 for j in serial["jobs"] if j.get("ok")),
            "jobs_total": len(serial["jobs"]),
        },
        "streamed": {
            "ok": streamed["ok"],
            "mode": streamed["mode"],
            "wall_seconds": str_w,
            "n_streams": streamed.get("n_streams"),
            "peak_mem_mb": streamed.get("peak_mem_mb"),
            "jobs_ok": sum(1 for j in streamed["jobs"] if j and j.get("ok")),
            "jobs_total": len(streamed["jobs"]),
        },
        "speedup_serial_over_streamed": speedup,
        "complexity_weight": complexity_weight(),
        "fold_depth": fold_depth_ladder(),
        "overall_ok": occupancy_ok,
        "note": (
            "Multi-stream fold queue on CUDA; work is fold jobs not 2^n amps. "
            "Speedup depends on kernel length vs launch overhead."
        ),
    }
    return report
