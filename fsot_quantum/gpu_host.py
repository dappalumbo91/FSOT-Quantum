"""
GPU host bridge — **FSOT-owned path only** (FSOT-GPU doctrine).

Primary: `fsot_quantum.device` — collapse / pack / gates on torch device.
Custom CUDA C++ is **not** the pathway. Backends are optional speed adapters.

See docs/QUANTUM_PATHWAY.md.
"""

from __future__ import annotations

from typing import Sequence

from fsot_quantum.device import (
    backend_info,
    batch_collapse_field,
    collapse,
    consensus_ring,
    cx_pairs,
    neg_spins,
    pack_spins,
    prefer_device,
    smoke_device,
    unpack_spins,
)
from fsot_quantum.seeds import COLLAPSE_THRESHOLD

# Back-compat aliases used by scripts
collapse_batch_python = batch_collapse_field
cuda_available = lambda: prefer_device() == "cuda"  # noqa: E731


def pack_spins_python(spins: Sequence[int]) -> list[int]:
    return pack_spins(spins, device="cpu")


__all__ = [
    "backend_info",
    "prefer_device",
    "collapse",
    "pack_spins",
    "unpack_spins",
    "batch_collapse_field",
    "collapse_batch_python",
    "neg_spins",
    "cx_pairs",
    "consensus_ring",
    "smoke_device",
    "cuda_available",
    "COLLAPSE_THRESHOLD",
]
