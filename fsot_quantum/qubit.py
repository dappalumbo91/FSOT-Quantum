"""
FSOT trit register — alternative to complex Hilbert qubits.

State space per site: T = {−1, 0, +1} (spin down / superposed / spin up).
Continuous pre-collapse field lives in ℝ and collapses by C_eff·P_var.

No complex amplitudes. No free-parameter statevector norms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from fsot_quantum.seeds import COLLAPSE_THRESHOLD, MAX_TRITS_WORD, SEEDS
from fsot_quantum.trinary import (
    SPIN_DOWN,
    SPIN_UP,
    SUPERPOSED,
    collapse_scalar,
    pack_signed_u64,
    signed_to_code,
    unpack_signed_u64,
)


@dataclass
class TritRegister:
    """Bare-metal trinary quantum register (host view)."""

    spins: list[int]
    # Continuous fluid field (pre-collapse); length == n when used
    field: list[float] = field(default_factory=list)
    domain: str = "Quantum_Computing"

    def __post_init__(self) -> None:
        self.spins = [int(s) for s in self.spins]
        for s in self.spins:
            if s not in (-1, 0, 1):
                raise ValueError(f"spin must be in {{-1,0,+1}}, got {s}")
        if self.field and len(self.field) != len(self.spins):
            raise ValueError("field length must match spins")

    @property
    def n(self) -> int:
        return len(self.spins)

    @classmethod
    def zeros(cls, n: int, domain: str = "Quantum_Computing") -> "TritRegister":
        """All superposed (fluid quiet state)."""
        return cls(spins=[int(SUPERPOSED)] * n, domain=domain)

    @classmethod
    def all_up(cls, n: int, domain: str = "Quantum_Computing") -> "TritRegister":
        return cls(spins=[int(SPIN_UP)] * n, domain=domain)

    @classmethod
    def all_down(cls, n: int, domain: str = "Quantum_Computing") -> "TritRegister":
        return cls(spins=[int(SPIN_DOWN)] * n, domain=domain)

    @classmethod
    def from_bits(cls, bits: Sequence[int], domain: str = "Quantum_Computing") -> "TritRegister":
        """Map classical bits: 0→down, 1→up (no superposed)."""
        spins = [int(SPIN_UP) if b else int(SPIN_DOWN) for b in bits]
        return cls(spins=spins, domain=domain)

    def copy(self) -> "TritRegister":
        return TritRegister(
            spins=list(self.spins),
            field=list(self.field),
            domain=self.domain,
        )

    def pack_words(self) -> list[int]:
        """Pack spins into u64 words (pad superposed to 32-multiple)."""
        codes_spins = list(self.spins)
        pad = (-len(codes_spins)) % 32
        if pad:
            codes_spins.extend([0] * pad)
        words = []
        for i in range(0, len(codes_spins), 32):
            words.append(pack_signed_u64(codes_spins[i : i + 32]))
        return words

    @classmethod
    def from_packed(cls, words: Sequence[int], n: int, domain: str = "Quantum_Computing") -> "TritRegister":
        spins: list[int] = []
        for w in words:
            spins.extend(unpack_signed_u64(int(w)))
        return cls(spins=spins[:n], domain=domain)

    def codes(self) -> list[int]:
        return [signed_to_code(s) for s in self.spins]

    def ensure_field(self) -> list[float]:
        """Materialize continuous field from spins if absent."""
        if not self.field:
            self.field = continuous_field_from_spins(self.spins)
        return self.field


def continuous_field_from_spins(spins: Sequence[int]) -> list[float]:
    """
    Embed discrete spins into continuous fluid values.

    Uses only seed-derived magnitudes:
      ±1 → ±(C_eff)  (emergent / damped poles below full collapse thresh? )
      0  → 0

    Note: C_eff < C_eff·P_var for P_var < 1, so ±C_eff remains superposed
    under collapse until observer/valve push — correct FSOT continuum layer.
    For a hard pole embedding that collapses immediately, use ±1.0 * (thresh + eps).
    Default: soft embedding at ±c_eff (pre-collapse continuum).
    """
    c = SEEDS.c_eff
    out = []
    for s in spins:
        s = int(s)
        if s > 0:
            out.append(c)
        elif s < 0:
            out.append(-c)
        else:
            out.append(0.0)
    return out


def hard_embed_spins(spins: Sequence[int]) -> list[float]:
    """Hard poles outside collapse threshold (for deterministic measure of ±1)."""
    thr = COLLAPSE_THRESHOLD
    # thr + poof ensures strictly outside without free params
    mag = thr + SEEDS.poof
    out = []
    for s in spins:
        s = int(s)
        if s > 0:
            out.append(mag)
        elif s < 0:
            out.append(-mag)
        else:
            out.append(0.0)
    return out


def collapse_field(field: Sequence[float], threshold: float = COLLAPSE_THRESHOLD) -> list[int]:
    return [collapse_scalar(float(v), threshold) for v in field]


def preferred_word_width() -> int:
    """Metatron cube word: 3³ = 27 trits."""
    return MAX_TRITS_WORD
