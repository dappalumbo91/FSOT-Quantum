"""
Logical qubit encoding on FSOT multi-spin substrate.

Not full fault-tolerant surface-code FTQC. Seed-locked repetition + consensus
recovery (same consensus as fsot_lib / gates) — first step toward logical qubits.

Encoding (odd distance d, default d=3 from floor(pi)):
  |0>_L  →  (+1,+1,+1)   spin-up block
  |1>_L  →  (−1,−1,−1)   spin-down block
  super  →  (0,0,0)

Recovery: majority / consensus vote (no free syndrome weights).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from fsot_lib.seeds import SEEDS
from fsot_quantum.gates import consensus, neg


def logical_distance() -> int:
    """d = max(3, 2*floor(pi/2)+1) → odd distance from seeds only."""
    k = max(1, int(math.floor(float(SEEDS.pi) / 2.0)))  # 1
    return 2 * k + 1  # 3


@dataclass
class LogicalRegister:
    n_logical: int
    distance: int
    # physical spins length n_logical * distance
    physical: list[int]

    @classmethod
    def zeros(cls, n_logical: int, distance: int | None = None) -> "LogicalRegister":
        d = distance or logical_distance()
        return cls(n_logical=n_logical, distance=d, physical=[1] * (n_logical * d))

    def _slice(self, L: int) -> slice:
        d = self.distance
        return slice(L * d, (L + 1) * d)

    def encode(self, L: int, bit: int) -> None:
        """Encode classical bit into logical block L.
        bit 0 → all +1 (spin up); bit 1 → all −1 (spin down).
        """
        val = -1 if int(bit) else 1
        sl = self._slice(L)
        for i in range(sl.start, sl.stop):
            self.physical[i] = val

    def encode_super(self, L: int) -> None:
        sl = self._slice(L)
        for i in range(sl.start, sl.stop):
            self.physical[i] = 0

    def majority(self, block: Sequence[int]) -> int:
        """Majority vote: +1 / −1; ties → 0 (superposed)."""
        up = sum(1 for x in block if int(x) > 0)
        down = sum(1 for x in block if int(x) < 0)
        if up > down:
            return 1
        if down > up:
            return -1
        return 0

    def decode(self, L: int) -> int:
        sl = self._slice(L)
        return self.majority(self.physical[sl])

    def consensus_recover(self, L: int) -> int:
        """Pairwise consensus fold then majority."""
        sl = self._slice(L)
        block = list(self.physical[sl])
        if len(block) < 2:
            return self.majority(block)
        acc = block[0]
        for b in block[1:]:
            acc = consensus(acc, b) if acc != 0 else b
        # if consensus wiped to 0, fall back majority
        if acc == 0:
            return self.majority(block)
        return acc

    def inject_error(self, physical_index: int, kind: str = "flip") -> None:
        """Error model for tests (not a free fit — fixed flip)."""
        if kind == "flip":
            self.physical[physical_index] = neg(self.physical[physical_index])
        elif kind == "erase":
            self.physical[physical_index] = 0

    def logical_x(self, L: int) -> None:
        """Logical X: flip all physical spins in block."""
        sl = self._slice(L)
        for i in range(sl.start, sl.stop):
            self.physical[i] = neg(self.physical[i])


def logical_error_correction_selftest() -> dict:
    d = logical_distance()
    reg = LogicalRegister.zeros(1, d)
    reg.encode(0, 0)  # logical 0 → all +1
    # single flip error
    reg.inject_error(0, "flip")
    recovered = reg.consensus_recover(0)
    ok_single = recovered == 1  # still majority +1
    # two errors on d=3 may fail — document
    reg2 = LogicalRegister.zeros(1, d)
    reg2.encode(0, 1)
    reg2.inject_error(0, "flip")
    reg2.inject_error(1, "flip")
    rec2 = reg2.majority(reg2.physical[0:d])
    # two flips on |1>_L (all -1) → one -1 left → majority -1 still if only 2 of 3 flipped? 
    # all -1, flip 0 and 1 → +1,+1,-1 → majority +1 (logical flip) — expected fail for 2 errors
    return {
        "distance": d,
        "single_error_correct": ok_single,
        "two_error_decoded": rec2,
        "ok": ok_single and d >= 3,
        "note": "Repetition+consensus code; corrects floor((d-1)/2) flip errors",
    }
