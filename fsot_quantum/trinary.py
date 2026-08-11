"""
Trinary spin algebra — authority for FSOT-Quantum.

Signed spins (user / Lean / Zig doctrine):
  −1 = SpinDown
   0 = Superposed
  +1 = SpinUp

2-bit pack codes (FSOT-GPU / Lean Trinary.lean):
  0 = SpinDown, 1 = Superposed, 2 = SpinUp
  3 = illegal / reserved

Collapse threshold: C_eff · P_var (seed-derived only).
"""

from __future__ import annotations

from enum import IntEnum
from typing import Sequence

from fsot_quantum.seeds import COLLAPSE_THRESHOLD, STATES_PER_U64


class Spin(IntEnum):
    DOWN = -1
    SUPER = 0
    UP = 1


SPIN_DOWN = Spin.DOWN
SUPERPOSED = Spin.SUPER
SPIN_UP = Spin.UP


def collapse_scalar(value: float, threshold: float = COLLAPSE_THRESHOLD) -> int:
    """Continuous field → signed spin in {−1, 0, +1}."""
    if value > threshold:
        return int(SPIN_UP)
    if value < -threshold:
        return int(SPIN_DOWN)
    return int(SUPERPOSED)


def signed_to_code(s: int) -> int:
    """Signed spin → 2-bit pack code {0,1,2}."""
    if s < 0:
        return 0
    if s > 0:
        return 2
    return 1


def code_to_signed(code: int) -> int:
    """2-bit pack code → signed spin."""
    return {0: -1, 1: 0, 2: 1}[int(code)]


def neg(t: int) -> int:
    """Polarity flip: −t. Superposed stays 0."""
    return -int(t)


def abs0(t: int) -> int:
    """0 if superposed else 1 (activity class)."""
    return 0 if int(t) == 0 else 1


def consensus(a: int, b: int) -> int:
    """Agreement gate: a if a==b else 0."""
    a, b = int(a), int(b)
    return a if a == b else 0


def sum_sat(a: int, b: int) -> int:
    """Saturated sum clamped to {−1,0,+1}."""
    s = int(a) + int(b)
    if s > 1:
        return 1
    if s < -1:
        return -1
    return s


def pair(a: int, b: int) -> int:
    """Trinary product a·b (pair weight term)."""
    return int(a) * int(b)


def trit_similarity(a: Sequence[int], b: Sequence[int]) -> float:
    """Mean consensus: match +1, opposite −1, either superposed skip (0 contrib)."""
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    acc = 0
    counted = 0
    for i in range(n):
        ta, tb = int(a[i]), int(b[i])
        if ta == 0 or tb == 0:
            continue
        counted += 1
        acc += 1 if ta == tb else -1
    if counted == 0:
        return 0.0
    return acc / counted


def pack_u64(codes: Sequence[int]) -> int:
    """Pack 32 codes in {0,1,2} into one 64-bit word (2 bits each)."""
    if len(codes) != STATES_PER_U64:
        raise ValueError(f"need exactly {STATES_PER_U64} codes")
    w = 0
    for i, c in enumerate(codes):
        ci = int(c) & 0x3
        if ci == 3:
            raise ValueError("illegal pack code 3")
        w |= ci << (2 * i)
    return w


def unpack_u64(word: int) -> list[int]:
    return [(int(word) >> (2 * i)) & 0x3 for i in range(STATES_PER_U64)]


def pack_signed_u64(spins: Sequence[int]) -> int:
    return pack_u64([signed_to_code(s) for s in spins])


def unpack_signed_u64(word: int) -> list[int]:
    return [code_to_signed(c) for c in unpack_u64(word)]


def pack_roundtrip_ok(codes: Sequence[int]) -> bool:
    return unpack_u64(pack_u64(list(codes))) == list(codes)
