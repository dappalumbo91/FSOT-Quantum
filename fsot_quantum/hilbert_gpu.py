"""
GPU Hilbert statevector — torch CUDA path (FSOT-GPU doctrine: device = speed).

Same seed-locked gates as hilbert.py; amplitudes live on prefer_device().
Uses free GPU headroom for n up to ~16–18 (memory-bound) and batch jobs.
"""

from __future__ import annotations

import math
import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.hilbert import ANGLES


def _torch():
    import torch

    return torch


class StatevectorGPU:
    """Normalized complex state on CUDA/CPU torch tensor, length 2^n."""

    def __init__(self, n: int, amps=None, device: str | None = None):
        torch = _torch()
        self.n = n
        self.device = device or prefer_device()
        dim = 1 << n
        if amps is None:
            self.amps = torch.zeros(dim, dtype=torch.complex128, device=self.device)
            self.amps[0] = 1.0 + 0j
        else:
            self.amps = torch.as_tensor(amps, dtype=torch.complex128, device=self.device)
            if self.amps.numel() != dim:
                raise ValueError("bad dim")
        self.normalize_()

    @classmethod
    def zeros(cls, n: int, device: str | None = None) -> "StatevectorGPU":
        return cls(n=n, device=device)

    @classmethod
    def basis(cls, n: int, index: int, device: str | None = None) -> "StatevectorGPU":
        torch = _torch()
        dev = device or prefer_device()
        amps = torch.zeros(1 << n, dtype=torch.complex128, device=dev)
        amps[index] = 1.0 + 0j
        return cls(n=n, amps=amps, device=dev)

    def normalize_(self) -> None:
        torch = _torch()
        nrm = torch.sqrt(torch.sum(torch.abs(self.amps) ** 2))
        if float(nrm) > 0:
            self.amps = self.amps / nrm

    def probs(self):
        torch = _torch()
        return (torch.abs(self.amps) ** 2).real

    def fidelity(self, other: "StatevectorGPU") -> float:
        torch = _torch()
        ov = torch.sum(torch.conj(self.amps) * other.amps)
        return float(torch.abs(ov) ** 2)

    def apply_1q(self, q: int, u00, u01, u10, u11) -> None:
        torch = _torch()
        n, amps = self.n, self.amps
        dim = 1 << n
        bit = 1 << q
        # reshape as (..., 2, ...) along qubit q
        # general: view as [2]*n is heavy; use mask indexing vectorized
        idx = torch.arange(dim, device=amps.device)
        lo = idx & ~bit
        # unique lo where bit clear
        mask0 = (idx & bit) == 0
        i0 = idx[mask0]
        i1 = i0 | bit
        a = amps[i0]
        b = amps[i1]
        out = amps.clone()
        out[i0] = u00 * a + u01 * b
        out[i1] = u10 * a + u11 * b
        self.amps = out

    def H(self, q: int) -> "StatevectorGPU":
        s = math.sqrt(0.5)
        self.apply_1q(q, s, s, s, -s)
        return self

    def X(self, q: int) -> "StatevectorGPU":
        self.apply_1q(q, 0, 1, 1, 0)
        return self

    def T(self, q: int) -> "StatevectorGPU":
        torch = _torch()
        phase = torch.exp(
            torch.tensor(1j * ANGLES["quarter_pi"], dtype=torch.complex128, device=self.device)
        )
        self.apply_1q(q, 1, 0, 0, phase)
        return self

    def S(self, q: int) -> "StatevectorGPU":
        self.apply_1q(q, 1, 0, 0, 1j)
        return self

    def CNOT(self, c: int, t: int) -> "StatevectorGPU":
        torch = _torch()
        n, amps = self.n, self.amps
        dim = 1 << n
        cb, tb = 1 << c, 1 << t
        idx = torch.arange(dim, device=amps.device)
        # when control set, swap with target flip
        ctrl = (idx & cb) != 0
        out = amps.clone()
        # for controlled bits: scatter from idx to idx^tb
        src = idx[ctrl]
        dst = src ^ tb
        out[dst] = amps[src]
        # non-control unchanged already in clone... but overwrote only dst from src
        # entries with ctrl that are dst of others handled; non-ctrl stay from clone
        # fix: rebuild
        out = torch.zeros_like(amps)
        out[~ctrl] = amps[~ctrl]
        out[dst] = amps[src]
        self.amps = out
        return self

    def cphase(self, c: int, t: int, angle: float) -> "StatevectorGPU":
        torch = _torch()
        n, amps = self.n, self.amps
        dim = 1 << n
        cb, tb = 1 << c, 1 << t
        idx = torch.arange(dim, device=amps.device)
        both = ((idx & cb) != 0) & ((idx & tb) != 0)
        ph = torch.exp(torch.tensor(1j * angle, dtype=torch.complex128, device=self.device))
        out = amps.clone()
        out[both] = amps[both] * ph
        self.amps = out
        return self


def apply_qft_gpu(sv: StatevectorGPU) -> StatevectorGPU:
    pi = float(SEEDS.pi)
    n = sv.n
    for i in range(n):
        sv.H(i)
        for j in range(i + 1, n):
            k = j - i
            angle = 2.0 * pi / (2**k)
            sv.cphase(j, i, angle)
    # bit reverse swaps via 3 CNOT
    for i in range(n // 2):
        a, b = i, n - 1 - i
        sv.CNOT(a, b)
        sv.CNOT(b, a)
        sv.CNOT(a, b)
    sv.normalize_()
    return sv


def ghz_gpu(n: int, device: str | None = None) -> StatevectorGPU:
    s = StatevectorGPU.zeros(n, device=device)
    s.H(0)
    for i in range(n - 1):
        s.CNOT(i, i + 1)
    s.normalize_()
    return s


def clifford_t_gpu(n: int, device: str | None = None) -> StatevectorGPU:
    depth = max(1, int(math.floor(float(SEEDS.pi))))
    layers = max(2, int(math.floor(float(SEEDS.e))))
    s = StatevectorGPU.zeros(n, device=device)
    for L in range(layers):
        for q in range(n):
            s.H(q)
            if (q + L) % 2 == 0:
                s.T(q)
            else:
                s.S(q)
        for q in range(n - 1):
            s.CNOT(q, q + 1)
        for q in range(n - 2, -1, -1):
            s.CNOT(q, q + 1)
        for _ in range(depth - 1):
            for q in range(n):
                s.T(q)
    s.normalize_()
    return s


def batch_ghz_stack(n: int, batch: int, device: str | None = None) -> dict[str, Any]:
    """
    Stack B independent |0>^n states and apply identical GHZ circuit in a loop
    on-device (keeps GPU busy; not a single fused kernel but sustained load).
    """
    torch = _torch()
    dev = device or prefer_device()
    if dev == "cuda":
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
    t0 = time.perf_counter()
    # Allocate B full statevectors on device and evolve each
    dim = 1 << n
    stack = torch.zeros(batch, dim, dtype=torch.complex128, device=dev)
    stack[:, 0] = 1.0 + 0j
    # Apply H on qubit 0 to all batch items via matrix-free indexing
    s = math.sqrt(0.5)
    bit = 1
    idx = torch.arange(dim, device=dev)
    mask0 = (idx & bit) == 0
    i0 = idx[mask0]
    i1 = i0 | bit
    for b in range(batch):
        a = stack[b, i0]
        bb = stack[b, i1]
        stack[b, i0] = s * a + s * bb
        stack[b, i1] = s * a - s * bb
        for q in range(n - 1):
            # CNOT q -> q+1
            cb, tb = 1 << q, 1 << (q + 1)
            idb = torch.arange(dim, device=dev)
            ctrl = (idb & cb) != 0
            src = idb[ctrl]
            dst = src ^ tb
            tmp = stack[b].clone()
            out = torch.zeros_like(tmp)
            out[~ctrl] = tmp[~ctrl]
            out[dst] = tmp[src]
            stack[b] = out
    # normalize each
    nrms = torch.sqrt(torch.sum(torch.abs(stack) ** 2, dim=1, keepdim=True))
    stack = stack / nrms.clamp_min(1e-30)
    if dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    # check first GHZ structure
    p = (torch.abs(stack[0]) ** 2).real
    ghz_ok = abs(float(p[0]) - 0.5) < 1e-6 and abs(float(p[-1]) - 0.5) < 1e-6
    mem = torch.cuda.max_memory_allocated() / (1024**2) if dev == "cuda" else None
    return {
        "job": f"batch_ghz_stack_n{n}_B{batch}",
        "device": dev,
        "n": n,
        "batch": batch,
        "dim": dim,
        "seconds": dt,
        "amps_per_sec": (batch * dim) / dt if dt > 0 else None,
        "circuits_per_sec": batch / dt if dt > 0 else None,
        "peak_mem_mb": mem,
        "ok": ghz_ok,
    }


def batch_pack_stress_gpu(n_groups: int = 1_000_000) -> dict[str, Any]:
    """Heavy pack roundtrip to load GPU memory bandwidth."""
    torch = _torch()
    from fsot_lib.trinary import pack_u64_torch, unpack_u64_torch

    dev = prefer_device()
    codes = torch.randint(0, 3, (n_groups, 32), device=dev, dtype=torch.uint8)
    if dev == "cuda":
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    packed = pack_u64_torch(codes)
    back = unpack_u64_torch(packed)
    if dev == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    ok = bool(torch.equal(codes, back))
    trits = n_groups * 32
    return {
        "device": dev,
        "groups": n_groups,
        "trits": trits,
        "seconds": dt,
        "trits_per_sec": trits / dt if dt > 0 else None,
        "ok": ok,
    }


def run_gpu_headroom_panel() -> dict[str, Any]:
    """
    Intentionally load the GPU: large pack, multi-n Hilbert, batched GHZ/QFT.
    """
    torch = _torch()
    dev = prefer_device()
    rows: list[dict[str, Any]] = []

    # Memory / bandwidth hammer
    for g in (250_000, 1_000_000, 4_000_000):
        try:
            r = batch_pack_stress_gpu(g)
            rows.append({"job": f"pack_{g}", **r})
        except RuntimeError as e:
            rows.append({"job": f"pack_{g}", "ok": False, "error": str(e), "device": dev})

    # Hilbert on GPU for increasing n
    for n in (8, 10, 12, 14, 16):
        try:
            if dev == "cuda":
                torch.cuda.synchronize()
                torch.cuda.reset_peak_memory_stats()
            t0 = time.perf_counter()
            g = ghz_gpu(n, device=dev)
            q = StatevectorGPU.zeros(n, device=dev)
            apply_qft_gpu(q)
            ct = clifford_t_gpu(n, device=dev)
            if dev == "cuda":
                torch.cuda.synchronize()
            dt = time.perf_counter() - t0
            # structure checks
            pg = g.probs()
            ghz_ok = abs(float(pg[0]) - 0.5) < 1e-8 and abs(float(pg[-1]) - 0.5) < 1e-8
            uni = torch.allclose(q.probs(), torch.full_like(q.probs(), 1.0 / (1 << n)), atol=1e-8)
            nrm = float(torch.sum(torch.abs(ct.amps) ** 2).real)
            mem = None
            if dev == "cuda":
                mem = torch.cuda.max_memory_allocated() / (1024**2)
            rows.append({
                "job": f"hilbert_n{n}",
                "device": dev,
                "n": n,
                "dim": 1 << n,
                "seconds": dt,
                "ghz_ok": ghz_ok,
                "qft_uniform": bool(uni),
                "clifford_norm": nrm,
                "ok": ghz_ok and bool(uni) and abs(nrm - 1.0) < 1e-8,
                "peak_mem_mb": mem,
            })
        except RuntimeError as e:
            rows.append({"job": f"hilbert_n{n}", "ok": False, "error": str(e), "n": n, "device": dev})

    # Sustained GPU load: stacked batch GHZ
    for n, B in ((8, 256), (10, 128), (12, 64), (14, 16)):
        try:
            rows.append(batch_ghz_stack(n, B, device=dev))
        except RuntimeError as e:
            rows.append({"job": f"batch_ghz_stack_n{n}_B{B}", "ok": False, "error": str(e)})

    # Grover-scale collapse field (already heavy)
    from fsot_quantum.gpu_parallel import batch_grover_search

    gr = batch_grover_search(8192, [(i * 97 + 3) % 8192 for i in range(1024)])
    rows.append({"job": "grover_batch_8k_x1024", **gr})

    overall = all(r.get("ok", False) for r in rows)
    # GPU utilization proxy metrics
    hilbert_rows = [r for r in rows if str(r.get("job", "")).startswith("hilbert_n")]
    pack_rows = [r for r in rows if str(r.get("job", "")).startswith("pack_")]

    report = {
        "panel": "gpu_headroom",
        "device": dev,
        "gpu_name": torch.cuda.get_device_name(0) if dev == "cuda" else None,
        "instances": rows,
        "overall_ok": overall,
        "highlights": {
            "max_hilbert_n": max((r.get("n") or 0 for r in hilbert_rows if r.get("ok")), default=0),
            "max_peak_mem_mb": max((r.get("peak_mem_mb") or 0 for r in hilbert_rows), default=0),
            "max_pack_trits_per_sec": max(
                (r.get("trits_per_sec") or 0 for r in pack_rows if r.get("ok")),
                default=0,
            ),
            "grover_ips": gr.get("instances_per_sec"),
        },
        "note": "Loads GPU with pack + Hilbert n<=16 + batches; watch nvidia-smi for util%",
    }
    return report
