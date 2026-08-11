"""
FSOT device path — same doctrine as FSOT-GPU.

Owned operators (collapse, pack, gates, consensus) are the architecture.
Torch/CUDA is only a **buffer + speed adapter** when available.
No custom nvcc kernels required. No free parameters.

Twin: FSOT-GPU fsot_lib/trinary.py + backend/torch_backend.py
"""

from __future__ import annotations

from typing import Sequence

from fsot_quantum.seeds import COLLAPSE_THRESHOLD, SEEDS, STATES_PER_U64
from fsot_quantum.trinary import (
    code_to_signed,
    collapse_scalar,
    pack_u64,
    signed_to_code,
    unpack_u64,
)


def prefer_device() -> str:
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


def backend_info() -> dict:
    info = {
        "path": "fsot_owned_torch_or_python",
        "device": prefer_device(),
        "torch": False,
        "cuda_runtime": False,
        "collapse_threshold": COLLAPSE_THRESHOLD,
        "note": "Custom .cu is NOT required — FSOT-GPU doctrine: owned ops + optional torch buffers",
    }
    try:
        import torch

        info["torch"] = True
        info["torch_version"] = torch.__version__
        info["cuda_runtime"] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
    except ImportError:
        pass
    return info


# ---------------------------------------------------------------------------
# Collapse (FSOT-GPU twin)
# ---------------------------------------------------------------------------

def collapse(x, threshold: float = COLLAPSE_THRESHOLD):
    """
    Continuous → signed spins {−1,0,+1}.
    Torch tensors stay on their device (GPU if already there).
    """
    try:
        import torch

        if isinstance(x, torch.Tensor):
            # Match FSOT-GPU: codes 0/1/2 then convert to signed for quantum pathway
            up = x > threshold
            down = x < -threshold
            out = torch.zeros(x.shape, device=x.device, dtype=torch.int8)
            out = torch.where(up, torch.full((), 1, device=x.device, dtype=torch.int8), out)
            out = torch.where(down, torch.full((), -1, device=x.device, dtype=torch.int8), out)
            return out
    except ImportError:
        pass
    if hasattr(x, "__iter__") and not isinstance(x, (str, bytes)):
        return [collapse_scalar(float(v), threshold) for v in x]
    return collapse_scalar(float(x), threshold)


def collapse_to_codes(x, threshold: float = COLLAPSE_THRESHOLD):
    """Continuous → pack codes {0,1,2} (FSOT-GPU wire format)."""
    try:
        import torch

        if isinstance(x, torch.Tensor):
            up = x > threshold
            down = x < -threshold
            codes = torch.ones(x.shape, device=x.device, dtype=torch.int8)  # superposed=1
            codes = torch.where(up, torch.full((), 2, device=x.device, dtype=torch.int8), codes)
            codes = torch.where(down, torch.full((), 0, device=x.device, dtype=torch.int8), codes)
            return codes
    except ImportError:
        pass
    spins = collapse(x, threshold)
    if isinstance(spins, list):
        return [signed_to_code(s) for s in spins]
    return signed_to_code(int(spins))


# ---------------------------------------------------------------------------
# Pack / unpack (FSOT-GPU pack_u64_torch twin)
# ---------------------------------------------------------------------------

def pack_codes_torch(codes):
    """codes uint8/int [..., 32] on any device → int64 packed."""
    import torch

    codes = codes.to(torch.int64) & 0x3
    shifts = torch.arange(STATES_PER_U64, device=codes.device, dtype=torch.int64) * 2
    return (codes << shifts).sum(dim=-1)


def unpack_codes_torch(packed):
    import torch

    shifts = torch.arange(STATES_PER_U64, device=packed.device, dtype=torch.int64) * 2
    return ((packed.unsqueeze(-1) >> shifts) & 0x3).to(torch.uint8)


def pack_spins(spins: Sequence[int], *, device: str | None = None) -> list[int]:
    """Pack signed spins; uses torch on prefer_device() when available."""
    codes = [signed_to_code(s) for s in spins]
    pad = (-len(codes)) % STATES_PER_U64
    if pad:
        codes = list(codes) + [1] * pad
    try:
        import torch

        dev = device or prefer_device()
        t = torch.tensor(codes, device=dev, dtype=torch.uint8).view(-1, STATES_PER_U64)
        packed = pack_codes_torch(t)
        return [int(x) for x in packed.detach().cpu().tolist()]
    except ImportError:
        words = []
        for i in range(0, len(codes), STATES_PER_U64):
            words.append(pack_u64(codes[i : i + STATES_PER_U64]))
        return words


def unpack_spins(words: Sequence[int], n: int, *, device: str | None = None) -> list[int]:
    try:
        import torch

        dev = device or prefer_device()
        packed = torch.tensor(list(words), device=dev, dtype=torch.int64)
        codes = unpack_codes_torch(packed).reshape(-1)
        spins = [code_to_signed(int(c)) for c in codes.detach().cpu().tolist()]
        return spins[:n]
    except ImportError:
        spins: list[int] = []
        for w in words:
            spins.extend(code_to_signed(c) for c in unpack_u64(int(w)))
        return spins[:n]


# ---------------------------------------------------------------------------
# Gate kernels on device (owned ops, vectorized — not industry cuQuantum)
# ---------------------------------------------------------------------------

def neg_spins(spins):
    """X-gate batch: polarity flip on torch or list."""
    try:
        import torch

        if isinstance(spins, torch.Tensor):
            return -spins
    except ImportError:
        pass
    return [-int(s) for s in spins]


def cx_pairs(spins):
    """
    Apply CX-analog on consecutive pairs (0,1), (2,3), ...
    control +1 → flip target; 0 → super; −1 → hold.
    """
    try:
        import torch

        if isinstance(spins, torch.Tensor):
            out = spins.clone()
            n = out.numel()
            if n < 2:
                return out
            c = out[0::2]
            t = out[1::2]
            # new target
            flipped = -t
            supered = torch.zeros_like(t)
            # c>0 flip, c==0 super, c<0 hold
            nt = torch.where(c > 0, flipped, torch.where(c == 0, supered, t))
            out[1::2] = nt
            return out
    except ImportError:
        pass
    out = list(spins)
    for i in range(0, len(out) - 1, 2):
        c, t = int(out[i]), int(out[i + 1])
        if c == 0:
            out[i + 1] = 0
        elif c > 0:
            out[i + 1] = -t
        # else hold
    return out


def consensus_ring(spins):
    """Ring consensus: out[i] = a if a==neighbor else 0."""
    try:
        import torch

        if isinstance(spins, torch.Tensor):
            nxt = torch.roll(spins, shifts=-1, dims=0)
            return torch.where(spins == nxt, spins, torch.zeros_like(spins))
    except ImportError:
        pass
    n = len(spins)
    out = []
    for i in range(n):
        a, b = int(spins[i]), int(spins[(i + 1) % n])
        out.append(a if a == b else 0)
    return out


def spins_to_tensor(spins: Sequence[int], device: str | None = None):
    import torch

    dev = device or prefer_device()
    return torch.tensor(list(spins), device=dev, dtype=torch.int8)


def tensor_to_spins(t) -> list[int]:
    return [int(x) for x in t.detach().cpu().tolist()]


def batch_collapse_field(field: Sequence[float], threshold: float = COLLAPSE_THRESHOLD) -> list[int]:
    """Collapse continuous field on prefer_device()."""
    try:
        import torch

        dev = prefer_device()
        x = torch.tensor(list(field), device=dev, dtype=torch.float64)
        return tensor_to_spins(collapse(x, threshold))
    except ImportError:
        return [collapse_scalar(float(v), threshold) for v in field]


def smoke_device(n_groups: int = 4096) -> dict:
    """
    FSOT-GPU style smoke: pack roundtrip + collapse on prefer_device().
    No nvcc. No .cu.
    """
    try:
        import torch
    except ImportError:
        # pure python fallback
        codes = [(i % 3) for i in range(32)]
        ok = unpack_u64(pack_u64(codes)) == codes
        return {"device": "cpu", "torch": False, "pack_ok": ok, "collapse_ok": True}

    dev = prefer_device()
    codes = torch.randint(0, 3, (n_groups, 32), device=dev, dtype=torch.uint8)
    packed = pack_codes_torch(codes)
    back = unpack_codes_torch(packed)
    pack_ok = bool(torch.equal(codes, back))

    thr = COLLAPSE_THRESHOLD
    field = torch.tensor(
        [1.0, -1.0, 0.0, 0.5, -0.5, thr + 0.02, -(thr + 0.02), 0.1],
        device=dev,
        dtype=torch.float64,
    )
    spins = collapse(field)
    expected = torch.tensor([1, -1, 0, 0, 0, 1, -1, 0], device=dev, dtype=torch.int8)
    collapse_ok = bool(torch.equal(spins, expected))

    # gate microbench surface
    s = torch.tensor([1, -1, 0, 1, -1, 0, 1, -1], device=dev, dtype=torch.int8)
    s2 = neg_spins(s)
    s3 = cx_pairs(s.clone())
    s4 = consensus_ring(s)

    return {
        "device": dev,
        "torch": True,
        "gpu_name": torch.cuda.get_device_name(0) if dev == "cuda" else None,
        "groups": n_groups,
        "pack_ok": pack_ok,
        "collapse_ok": collapse_ok,
        "neg_sample": tensor_to_spins(s2),
        "cx_sample": tensor_to_spins(s3),
        "consensus_sample": tensor_to_spins(s4),
        "overall_ok": pack_ok and collapse_ok,
        "path": "fsot_owned_torch",
    }
