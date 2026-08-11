"""
Trinary quantum register on FSOT-GPU contracts.

Continuous fluid field + collapse via fsot_lib.trinary.collapse.
Signed spins: −1 / 0 / +1. Pack codes via fsot_lib pack_u64.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import (
    code_to_signed,
    collapse,
    pack_u64,
    signed_to_code,
    unpack_u64,
)


def codes_to_signed(codes: Sequence[int]) -> list[int]:
    return [code_to_signed(int(c)) for c in codes]


def signed_to_codes(spins: Sequence[int]) -> list[int]:
    return [signed_to_code(int(s)) for s in spins]


@dataclass
class TritRegister:
    """n-site FSOT trit register (host). Optional continuous field for collapse."""

    spins: list[int]  # signed −1,0,+1
    field: list[float] = field(default_factory=list)
    domain: str = "Quantum_Computing"

    def __post_init__(self) -> None:
        self.spins = [int(s) for s in self.spins]
        for s in self.spins:
            if s not in (-1, 0, 1):
                raise ValueError(f"spin must be −1/0/+1, got {s}")
        if self.field and len(self.field) != len(self.spins):
            raise ValueError("field length must match spins")

    @property
    def n(self) -> int:
        return len(self.spins)

    @classmethod
    def zeros(cls, n: int, domain: str = "Quantum_Computing") -> "TritRegister":
        return cls(spins=[0] * n, domain=domain)

    @classmethod
    def from_bits(cls, bits: Sequence[int], domain: str = "Quantum_Computing") -> "TritRegister":
        # classical 0 → down (−1), 1 → up (+1)
        return cls(spins=[1 if b else -1 for b in bits], domain=domain)

    @classmethod
    def from_codes(cls, codes: Sequence[int], domain: str = "Quantum_Computing") -> "TritRegister":
        return cls(spins=codes_to_signed(codes), domain=domain)

    def copy(self) -> "TritRegister":
        return TritRegister(list(self.spins), list(self.field), self.domain)

    def codes(self) -> list[int]:
        return signed_to_codes(self.spins)

    def pack_words(self) -> list[int]:
        codes = self.codes()
        pad = (-len(codes)) % 32
        if pad:
            codes = codes + [1] * pad
        return [pack_u64(codes[i : i + 32]) for i in range(0, len(codes), 32)]

    def materialize_field(self) -> list[float]:
        """Soft continuum embed at ±c_eff (below full collapse poles)."""
        c = SEEDS.c_eff
        self.field = [c if s > 0 else (-c if s < 0 else 0.0) for s in self.spins]
        return self.field

    def collapse_field(self) -> "TritRegister":
        """Apply fsot_lib.collapse on field → update spins."""
        if not self.field:
            self.materialize_field()
        codes = collapse(self.field)
        if hasattr(codes, "tolist"):
            codes = codes.tolist()
        # collapse returns codes 0/1/2 when torch; pure path may return list of codes
        # fsot_lib.collapse pure returns list of codes 0/1/2
        if codes and int(codes[0]) in (0, 1, 2) and all(int(c) in (0, 1, 2) for c in codes):
            self.spins = codes_to_signed([int(c) for c in codes])
        else:
            # already signed
            self.spins = [int(c) for c in codes]
        return self
