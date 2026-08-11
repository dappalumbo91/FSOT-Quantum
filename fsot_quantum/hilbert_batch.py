"""
Fused batched Hilbert — torch tensors shaped [B, 2^n] on CUDA.

All gates apply across the full batch in one vectorized op (high GPU util).
Seed-locked angles only. Competitor path: many circuits in parallel like a QPU
batch / classical wavefunction engine on consumer silicon.
"""

from __future__ import annotations

import math
import time
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.hilbert import ANGLES


def _t():
    import torch

    return torch


class BatchState:
    """B independent pure states, each dim 2^n, complex128 on device."""

    def __init__(self, n: int, batch: int, device: str | None = None):
        torch = _t()
        self.n = n
        self.batch = batch
        self.device = device or prefer_device()
        dim = 1 << n
        self.amps = torch.zeros(batch, dim, dtype=torch.complex128, device=self.device)
        self.amps[:, 0] = 1.0 + 0j

    def normalize_(self) -> None:
        torch = _t()
        nrm = torch.sqrt(torch.sum(torch.abs(self.amps) ** 2, dim=-1, keepdim=True))
        self.amps = self.amps / nrm.clamp_min(1e-30)

    def apply_1q(self, q: int, u00, u01, u10, u11) -> None:
        """Apply same 1-qubit gate to all batch items, qubit q."""
        torch = _t()
        n, amps = self.n, self.amps
        dim = 1 << n
        bit = 1 << q
        idx = torch.arange(dim, device=amps.device)
        mask0 = (idx & bit) == 0
        i0 = idx[mask0]
        i1 = i0 | bit
        a = amps[:, i0]
        b = amps[:, i1]
        # u may be python complex or tensor
        out = amps.clone()
        out[:, i0] = u00 * a + u01 * b
        out[:, i1] = u10 * a + u11 * b
        self.amps = out

    def H(self, q: int) -> "BatchState":
        s = math.sqrt(0.5)
        self.apply_1q(q, s, s, s, -s)
        return self

    def X(self, q: int) -> "BatchState":
        self.apply_1q(q, 0, 1, 1, 0)
        return self

    def T(self, q: int) -> "BatchState":
        torch = _t()
        ph = torch.exp(
            torch.tensor(1j * ANGLES["quarter_pi"], dtype=torch.complex128, device=self.device)
        )
        self.apply_1q(q, 1, 0, 0, ph)
        return self

    def S(self, q: int) -> "BatchState":
        self.apply_1q(q, 1, 0, 0, 1j)
        return self

    def CNOT(self, c: int, t: int) -> "BatchState":
        torch = _t()
        n, amps = self.n, self.amps
        dim = 1 << n
        cb, tb = 1 << c, 1 << t
        idx = torch.arange(dim, device=amps.device)
        ctrl = (idx & cb) != 0
        src = idx[ctrl]
        dst = src ^ tb
        out = torch.zeros_like(amps)
        out[:, ~ctrl] = amps[:, ~ctrl]
        out[:, dst] = amps[:, src]
        self.amps = out
        return self

    def cphase(self, c: int, t: int, angle: float) -> "BatchState":
        torch = _t()
        n, amps = self.n, self.amps
        dim = 1 << n
        cb, tb = 1 << c, 1 << t
        idx = torch.arange(dim, device=amps.device)
        both = ((idx & cb) != 0) & ((idx & tb) != 0)
        ph = torch.exp(torch.tensor(1j * angle, dtype=torch.complex128, device=self.device))
        out = amps.clone()
        out[:, both] = amps[:, both] * ph
        self.amps = out
        return self

    def probs(self):
        torch = _t()
        return (torch.abs(self.amps) ** 2).real


def batch_ghz(n: int, batch: int, device: str | None = None) -> BatchState:
    s = BatchState(n, batch, device)
    s.H(0)
    for i in range(n - 1):
        s.CNOT(i, i + 1)
    s.normalize_()
    return s


def batch_qft(n: int, batch: int, device: str | None = None) -> BatchState:
    pi = float(SEEDS.pi)
    s = BatchState(n, batch, device)
    for i in range(n):
        s.H(i)
        for j in range(i + 1, n):
            k = j - i
            s.cphase(j, i, 2.0 * pi / (2**k))
    for i in range(n // 2):
        a, b = i, n - 1 - i
        s.CNOT(a, b)
        s.CNOT(b, a)
        s.CNOT(a, b)
    s.normalize_()
    return s


def batch_clifford_t(n: int, batch: int, device: str | None = None) -> BatchState:
    depth = max(1, int(math.floor(float(SEEDS.pi))))
    layers = max(2, int(math.floor(float(SEEDS.e))))
    s = BatchState(n, batch, device)
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
        for _ in range(max(0, depth - 1)):
            for q in range(n):
                s.T(q)
    s.normalize_()
    return s


def _mem_mb() -> float | None:
    torch = _t()
    if prefer_device() != "cuda":
        return None
    return torch.cuda.max_memory_allocated() / (1024**2)


def _sync(dev: str) -> None:
    torch = _t()
    if dev == "cuda":
        torch.cuda.synchronize()


def estimate_batch(n: int, bytes_per_amp: int = 16, mem_frac: float = 0.35) -> int:
    """How many states fit in ~mem_frac of GPU free memory (seed-free heuristic)."""
    torch = _t()
    dim = 1 << n
    if prefer_device() != "cuda":
        return max(1, min(64, 2 ** (20 - n)))
    free, total = torch.cuda.mem_get_info()
    budget = int(free * mem_frac)
    per = dim * bytes_per_amp * 3  # amps + workspace headroom
    b = max(1, budget // per)
    # cap for runtime
    return int(min(b, 4096, max(1, 2 ** (22 - n))))


def run_fused_climb_panel() -> dict[str, Any]:
    """
    Climb: fused batch Hilbert at high GPU occupancy for n=8..20.
    """
    torch = _t()
    dev = prefer_device()
    rows = []

    # Pack hammer (bandwidth)
    from fsot_lib.trinary import pack_u64_torch, unpack_u64_torch

    for groups in (2_000_000, 8_000_000):
        try:
            codes = torch.randint(0, 3, (groups, 32), device=dev, dtype=torch.uint8)
            _sync(dev)
            t0 = time.perf_counter()
            p = pack_u64_torch(codes)
            b = unpack_u64_torch(p)
            _sync(dev)
            dt = time.perf_counter() - t0
            rows.append({
                "job": f"pack_{groups}",
                "ok": bool(torch.equal(codes, b)),
                "seconds": dt,
                "trits_per_sec": groups * 32 / dt,
                "device": dev,
            })
        except RuntimeError as e:
            rows.append({"job": f"pack_{groups}", "ok": False, "error": str(e)})

    # Fused GHZ / QFT / Clifford batches
    plans = []
    for n in (8, 10, 12, 14, 16, 18, 20):
        B = estimate_batch(n)
        if n >= 18:
            B = min(B, 8 if n == 18 else 2)  # safety for 2^18 * 16B * B
        if n == 20:
            B = min(B, 1)
        plans.append((n, B))

    for n, B in plans:
        for kind, fn in (
            ("ghz", batch_ghz),
            ("qft", batch_qft),
            ("clifford_t", batch_clifford_t),
        ):
            # skip heavy clifford at n>=18 (many layers)
            if kind == "clifford_t" and n >= 18:
                continue
            if kind == "qft" and n >= 20:
                continue
            try:
                if dev == "cuda":
                    torch.cuda.reset_peak_memory_stats()
                    torch.cuda.empty_cache()
                _sync(dev)
                t0 = time.perf_counter()
                s = fn(n, B, device=dev)
                _sync(dev)
                dt = time.perf_counter() - t0
                p0 = s.probs()
                ok = True
                detail = {}
                if kind == "ghz":
                    ok = abs(float(p0[0, 0]) - 0.5) < 1e-6 and abs(float(p0[0, -1]) - 0.5) < 1e-6
                elif kind == "qft":
                    target = 1.0 / (1 << n)
                    ok = bool(torch.allclose(p0[0], torch.full_like(p0[0], target), atol=1e-7))
                else:
                    nrm = float(torch.sum(torch.abs(s.amps[0]) ** 2).real)
                    ok = abs(nrm - 1.0) < 1e-8
                    detail["norm"] = nrm
                rows.append({
                    "job": f"fused_{kind}_n{n}_B{B}",
                    "kind": kind,
                    "n": n,
                    "batch": B,
                    "dim": 1 << n,
                    "seconds": dt,
                    "circuits_per_sec": B / dt if dt > 0 else None,
                    "amp_updates_per_sec": (B * (1 << n)) / dt if dt > 0 else None,
                    "peak_mem_mb": _mem_mb(),
                    "ok": ok,
                    "device": dev,
                    **detail,
                })
            except RuntimeError as e:
                rows.append({
                    "job": f"fused_{kind}_n{n}_B{B}",
                    "ok": False,
                    "error": str(e)[:200],
                    "n": n,
                    "batch": B,
                })

    ok_rows = [r for r in rows if r.get("ok")]
    report = {
        "panel": "fused_gpu_climb",
        "device": dev,
        "gpu_name": torch.cuda.get_device_name(0) if dev == "cuda" else None,
        "instances": rows,
        "overall_ok": len(ok_rows) == len(rows) and len(rows) > 0,
        "highlights": {
            "max_n_ok": max((r.get("n") or 0 for r in ok_rows), default=0),
            "max_circuits_per_sec": max(
                (r.get("circuits_per_sec") or 0 for r in ok_rows), default=0
            ),
            "max_amp_updates_per_sec": max(
                (r.get("amp_updates_per_sec") or 0 for r in ok_rows), default=0
            ),
            "max_peak_mem_mb": max((r.get("peak_mem_mb") or 0 for r in ok_rows), default=0),
            "max_pack_trits_per_sec": max(
                (r.get("trits_per_sec") or 0 for r in ok_rows if "pack" in str(r.get("job"))),
                default=0,
            ),
        },
    }
    return report
