"""
Multi-process fold scheduler — beyond single-device CUDA streams.

Workers run independent fold jobs in a process pool (CPU). GPU remains
optional per-process; default is host fold jobs so Windows spawn is safe.

Compares serial wall vs process-pool wall. Same QC *jobs*, fold geometry.

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import math
import os
import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import complexity_weight, fold_depth_ladder
from fsot_quantum.fold_jobs import (
    fold_factor,
    fold_ising_optimize,
    fold_marked_search,
    fold_period_finding,
    fold_secret_parity,
)


def _worker(task: dict[str, Any]) -> dict[str, Any]:
    kind = task["kind"]
    if kind == "search":
        r = fold_marked_search(int(task["n"]), int(task["marked"]))
    elif kind == "period":
        r = fold_period_finding(int(task["a"]), int(task["N"]))
    elif kind == "factor":
        r = fold_factor(int(task["N"]))
    elif kind == "bv":
        r = fold_secret_parity(list(task["secret"]))
    elif kind == "ising":
        n = int(task["n"])
        edges = [(i, (i + 1) % n, 1) for i in range(n)]
        r = fold_ising_optimize(n, edges)
    else:
        r = {"ok": False, "error": f"unknown kind {kind}"}
    r["task_id"] = task.get("id")
    r["kind"] = kind
    return r


def _task_bank() -> list[dict[str, Any]]:
    """Seed-locked task list — enough work to show process overlap."""
    tasks: list[dict[str, Any]] = []
    tid = 0
    phi = float(SEEDS.phi)
    for k in range(8):
        n = 2000 + k * 250
        marked = (int(phi * 1e6) * (k + 1)) % n
        tasks.append({"id": tid, "kind": "search", "n": n, "marked": marked})
        tid += 1
    for a, N in ((7, 15), (2, 15), (5, 21), (2, 33), (2, 35), (8, 51)):
        tasks.append({"id": tid, "kind": "period", "a": a, "N": N})
        tid += 1
    for N in (15, 21, 33, 35, 51, 65, 77, 91):
        tasks.append({"id": tid, "kind": "factor", "N": N})
        tid += 1
    tasks.append({"id": tid, "kind": "bv", "secret": [1, 0, 1, 1, 0, 1]})
    tid += 1
    for n in (8, 10, 12):
        tasks.append({"id": tid, "kind": "ising", "n": n})
        tid += 1
    return tasks


def _run_serial(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    t0 = time.perf_counter()
    rows = [_worker(t) for t in tasks]
    return {
        "mode": "serial",
        "wall_seconds": time.perf_counter() - t0,
        "ok": all(r.get("ok") for r in rows),
        "pass": f"{sum(1 for r in rows if r.get('ok'))}/{len(rows)}",
        "n_tasks": len(rows),
    }


def _run_pool(tasks: list[dict[str, Any]], workers: int) -> dict[str, Any]:
    from concurrent.futures import ProcessPoolExecutor

    t0 = time.perf_counter()
    try:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            rows = list(ex.map(_worker, tasks, chunksize=1))
        err = None
    except Exception as e:
        # Windows spawn / freeze issues → fail closed with reason
        return {
            "mode": "process_pool",
            "ok": False,
            "error": str(e)[:300],
            "workers": workers,
            "wall_seconds": time.perf_counter() - t0,
        }
    return {
        "mode": "process_pool",
        "workers": workers,
        "wall_seconds": time.perf_counter() - t0,
        "ok": all(r.get("ok") for r in rows),
        "pass": f"{sum(1 for r in rows if r.get('ok'))}/{len(rows)}",
        "n_tasks": len(rows),
    }


def run_fold_mp_scheduler_panel() -> dict[str, Any]:
    tasks = _task_bank()
    ncpu = os.cpu_count() or 2
    # seed-locked worker count: min(ncpu, floor(e)+2) → typically 4
    workers = max(2, min(ncpu, int(math.floor(float(SEEDS.e))) + 2))

    serial = _run_serial(tasks)
    pooled = _run_pool(tasks, workers)

    ser_w = serial["wall_seconds"]
    pool_w = pooled.get("wall_seconds") or 0.0
    speedup = ser_w / pool_w if pool_w > 0 else None

    # Gate: both correct; pool not catastrophically worse than 1/φ
    floor = 1.0 / float(SEEDS.phi)
    occupancy_ok = bool(serial.get("ok")) and bool(pooled.get("ok"))
    if speedup is not None:
        occupancy_ok = occupancy_ok and speedup >= floor

    return {
        "panel": "fold_mp_scheduler",
        "n_tasks": len(tasks),
        "ncpu": ncpu,
        "workers": workers,
        "serial": serial,
        "pooled": pooled,
        "speedup_serial_over_pool": speedup,
        "speedup_floor": floor,
        "complexity_weight": complexity_weight(),
        "fold_depth": fold_depth_ladder(),
        "overall_ok": occupancy_ok,
        "note": (
            "Process-pool fold jobs (search/period/factor/Ising) — "
            "not Hilbert 2^n tensors. Beyond CUDA streams."
        ),
    }
