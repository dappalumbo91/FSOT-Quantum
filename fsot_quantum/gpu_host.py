"""
Host bridge for CUDA kernels (optional).

Falls back to pure Python if the DLL is not built.
Bare-metal path: compile cuda/*.cu → fsot_quantum_cuda.dll / .so
"""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path
from typing import Sequence

from fsot_quantum.seeds import COLLAPSE_THRESHOLD, STATES_PER_U64
from fsot_quantum.trinary import (
    code_to_signed,
    collapse_scalar,
    pack_u64,
    signed_to_code,
    unpack_u64,
)

ROOT = Path(__file__).resolve().parents[1]
_DLL = None


def _dll_candidates() -> list[Path]:
    names = [
        "fsot_quantum_cuda.dll",
        "libfsot_quantum_cuda.dll",
        "libfsot_quantum_cuda.so",
        "fsot_quantum_cuda.so",
    ]
    dirs = [ROOT / "cuda", ROOT / "build", ROOT]
    out = []
    for d in dirs:
        for n in names:
            out.append(d / n)
    return out


def load_cuda_lib():
    global _DLL
    if _DLL is not None:
        return _DLL
    for p in _dll_candidates():
        if p.exists():
            _DLL = ctypes.CDLL(str(p))
            return _DLL
    return None


def pack_spins_python(spins: Sequence[int]) -> list[int]:
    codes = [signed_to_code(s) for s in spins]
    pad = (-len(codes)) % STATES_PER_U64
    if pad:
        codes = list(codes) + [1] * pad  # pad superposed
    words = []
    for i in range(0, len(codes), STATES_PER_U64):
        words.append(pack_u64(codes[i : i + STATES_PER_U64]))
    return words


def unpack_spins_python(words: Sequence[int], n: int) -> list[int]:
    spins: list[int] = []
    for w in words:
        spins.extend(code_to_signed(c) for c in unpack_u64(int(w)))
    return spins[:n]


def collapse_batch_python(field: Sequence[float], threshold: float = COLLAPSE_THRESHOLD) -> list[int]:
    return [collapse_scalar(float(v), threshold) for v in field]


def pack_spins(spins: Sequence[int]) -> list[int]:
    """Prefer CUDA pack when available; else Python."""
    lib = load_cuda_lib()
    if lib is None:
        return pack_spins_python(spins)
    # CUDA path expects flat codes then pack kernel — use Python host pack for ABI simplicity
    # Native device path is exercised by cuda smoke binary.
    return pack_spins_python(spins)


def cuda_available() -> bool:
    return load_cuda_lib() is not None


def backend_info() -> dict:
    return {
        "cuda_dll": cuda_available(),
        "dll_path": next((str(p) for p in _dll_candidates() if p.exists()), None),
        "python": sys.version.split()[0],
        "collapse_threshold": COLLAPSE_THRESHOLD,
    }
