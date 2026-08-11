"""
Mega-batch GPU occupancy panel — fill VRAM and SMs like a QC job queue.

Jobs:
  - large trit pack/unpack
  - fused Hilbert at max batch for n=8..16 + n=18/20
  - large Ising/MaxCut batches
  - surface spin hammer

Reports amp updates/s, pack trits/s, peak mem MB, estimated VRAM fraction.
"""

from __future__ import annotations

import math
import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.hilbert_batch import (
    BatchState,
    batch_ghz,
    batch_qft,
    batch_clifford_t,
    estimate_batch,
    _sync,
    _mem_mb,
)
from fsot_quantum.opt_gpu import batch_maxcut_local, _cycle_edges
from fsot_quantum.surface_code import run_surface_code_gpu_batch


def _t():
    import torch

    return torch


def _vram_info():
    torch = _t()
    if prefer_device() != "cuda":
        return None, None
    free, total = torch.cuda.mem_get_info()
    return free, total


def run_mega_gpu_panel() -> dict[str, Any]:
    torch = _t()
    dev = prefer_device()
    rows = []

    free0, total = _vram_info()
    if dev == "cuda":
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()

    # 1) Pack hammer — 16M groups × 32 trits
    from fsot_lib.trinary import pack_u64_torch, unpack_u64_torch

    for groups in (4_000_000, 16_000_000):
        try:
            if dev == "cuda":
                torch.cuda.empty_cache()
            codes = torch.randint(0, 3, (groups, 32), device=dev, dtype=torch.uint8)
            _sync(dev)
            t0 = time.perf_counter()
            p = pack_u64_torch(codes)
            b = unpack_u64_torch(p)
            _sync(dev)
            dt = time.perf_counter() - t0
            rows.append({
                "job": f"mega_pack_{groups}",
                "ok": bool(torch.equal(codes, b)),
                "seconds": dt,
                "trits_per_sec": groups * 32 / dt if dt > 0 else 0,
                "peak_mem_mb": _mem_mb(),
                "device": dev,
            })
            del codes, p, b
        except RuntimeError as e:
            rows.append({"job": f"mega_pack_{groups}", "ok": False, "error": str(e)[:200]})

    # 2) Fused Hilbert — aggressive batches
    for n in (8, 10, 12, 14, 16, 18, 20):
        B = estimate_batch(n, mem_frac=0.45)
        if n >= 18:
            B = min(B, 16 if n == 18 else 2)
        if n == 20:
            B = min(B, 2)
        for kind, fn in (("ghz", batch_ghz), ("qft", batch_qft)):
            if kind == "qft" and n >= 20:
                continue
            try:
                if dev == "cuda":
                    torch.cuda.empty_cache()
                    torch.cuda.reset_peak_memory_stats()
                _sync(dev)
                t0 = time.perf_counter()
                s = fn(n, B, device=dev)
                _sync(dev)
                dt = time.perf_counter() - t0
                p0 = s.probs()
                if kind == "ghz":
                    ok = abs(float(p0[0, 0]) - 0.5) < 1e-6 and abs(float(p0[0, -1]) - 0.5) < 1e-6
                else:
                    target = 1.0 / (1 << n)
                    ok = bool(torch.allclose(p0[0], torch.full_like(p0[0], target), atol=1e-7))
                rows.append({
                    "job": f"mega_fused_{kind}_n{n}_B{B}",
                    "kind": kind,
                    "n": n,
                    "batch": B,
                    "ok": ok,
                    "seconds": dt,
                    "circuits_per_sec": B / dt if dt > 0 else 0,
                    "amp_updates_per_sec": (B * (1 << n)) / dt if dt > 0 else 0,
                    "peak_mem_mb": _mem_mb(),
                    "device": dev,
                })
                del s, p0
            except RuntimeError as e:
                rows.append({
                    "job": f"mega_fused_{kind}_n{n}_B{B}",
                    "ok": False,
                    "error": str(e)[:200],
                    "n": n,
                    "batch": B,
                })

    # 3) Deep Clifford-T at n=12 max batch (depth stress)
    try:
        n, B = 12, estimate_batch(12, mem_frac=0.4)
        B = min(B, 256)
        if dev == "cuda":
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        _sync(dev)
        t0 = time.perf_counter()
        s = batch_clifford_t(n, B, device=dev)
        _sync(dev)
        dt = time.perf_counter() - t0
        nrm = float(torch.sum(torch.abs(s.amps[0]) ** 2).real)
        rows.append({
            "job": f"mega_clifford_n{n}_B{B}",
            "ok": abs(nrm - 1.0) < 1e-8,
            "seconds": dt,
            "circuits_per_sec": B / dt if dt > 0 else 0,
            "amp_updates_per_sec": (B * (1 << n)) / dt if dt > 0 else 0,
            "peak_mem_mb": _mem_mb(),
            "device": dev,
        })
        del s
    except RuntimeError as e:
        rows.append({"job": "mega_clifford", "ok": False, "error": str(e)[:200]})

    # 4) Large MaxCut batches
    for n, B in ((32, 512), (48, 256), (64, 128), (96, 64)):
        edges = _cycle_edges(n)
        phi = float(SEEDS.phi)
        x = 1
        for k in range(n // 2):
            x = (x * int(phi * 1e6) + k * 2654435761) % (n * n)
            a, b = x % n, (x // n) % n
            if a != b:
                if a > b:
                    a, b = b, a
                edges.append((a, b, 1))
        edges = list({(a, b, 1) for a, b, _ in edges})
        try:
            r = batch_maxcut_local(n, edges, B)
            rows.append({"job": f"mega_maxcut_n{n}_B{B}", **r})
        except RuntimeError as e:
            rows.append({"job": f"mega_maxcut_n{n}_B{B}", "ok": False, "error": str(e)[:200]})

    # 5) Surface GPU batch
    surf = run_surface_code_gpu_batch()
    rows.append({"job": "surface_spin_batch", **{k: v for k, v in surf.items() if k != "panel"}})

    ok_rows = [r for r in rows if r.get("ok")]
    peak_mem = max((r.get("peak_mem_mb") or 0 for r in rows), default=0)
    vram_frac = (peak_mem / (total / (1024**2))) if total else None

    report = {
        "panel": "mega_gpu_occupancy",
        "device": dev,
        "gpu_name": torch.cuda.get_device_name(0) if dev == "cuda" else None,
        "vram_total_mb": total / (1024**2) if total else None,
        "instances": rows,
        "overall_ok": len(ok_rows) == len(rows) and len(rows) > 0,
        "highlights": {
            "max_amp_updates_per_sec": max(
                (r.get("amp_updates_per_sec") or 0 for r in ok_rows), default=0
            ),
            "max_circuits_per_sec": max(
                (r.get("circuits_per_sec") or 0 for r in ok_rows), default=0
            ),
            "max_pack_trits_per_sec": max(
                (r.get("trits_per_sec") or 0 for r in ok_rows), default=0
            ),
            "max_opt_ips": max(
                (r.get("instances_per_sec") or 0 for r in ok_rows if "maxcut" in str(r.get("job"))),
                default=0,
            ),
            "max_peak_mem_mb": peak_mem,
            "vram_frac_peak": vram_frac,
            "jobs_ok": f"{len(ok_rows)}/{len(rows)}",
        },
    }
    return report
