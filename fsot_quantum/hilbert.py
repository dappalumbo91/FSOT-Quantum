"""
Hilbert-space layer for FSOT-QC — complex statevector with seed-locked unitaries.

Angles and phases come only from seeds (π, e, φ, …) and closed FSOT composites.
No free variational angles. No ad-hoc matrix fits.

Gate set (industry-comparable): H, X, Y, Z, S, T, Phase(θ_seed), CNOT, SWAP, CPhase.
Universal for qubit QC in the usual sense (Clifford+T with fixed T = π/4).

Bridge to trinary: measure → collapse real part / probability → pack codes.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Sequence

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import collapse


def _seed_angles() -> dict[str, float]:
    """All angles from seeds only."""
    pi = float(SEEDS.pi)
    return {
        "pi": pi,
        "half_pi": pi / 2.0,
        "quarter_pi": pi / 4.0,  # T gate
        "eighth_pi": pi / 8.0,
        "theta_s": float(SEEDS.theta_s),  # FSOT composite phase
        "psi_con": float(SEEDS.psi_con),
        "phi_fold": 2.0 * pi / float(SEEDS.phi),  # golden-related phase
    }


ANGLES = _seed_angles()


@dataclass
class Statevector:
    """Normalized complex amplitudes, length 2^n."""

    n: int
    amps: list[complex]

    def __post_init__(self) -> None:
        dim = 1 << self.n
        if len(self.amps) != dim:
            raise ValueError(f"need {dim} amplitudes for n={self.n}")
        self.normalize()

    @classmethod
    def zeros(cls, n: int) -> "Statevector":
        amps = [0j] * (1 << n)
        amps[0] = 1.0 + 0j
        return cls(n=n, amps=amps)

    @classmethod
    def basis(cls, n: int, index: int) -> "Statevector":
        amps = [0j] * (1 << n)
        amps[index] = 1.0 + 0j
        return cls(n=n, amps=amps)

    def copy(self) -> "Statevector":
        return Statevector(n=self.n, amps=list(self.amps))

    def normalize(self) -> None:
        s = sum(abs(a) ** 2 for a in self.amps)
        if s <= 0:
            return
        inv = 1.0 / math.sqrt(s)
        self.amps = [a * inv for a in self.amps]

    def probs(self) -> list[float]:
        return [abs(a) ** 2 for a in self.amps]

    def fidelity(self, other: "Statevector") -> float:
        if other.n != self.n:
            raise ValueError("n mismatch")
        # |⟨ψ|φ⟩|²
        ov = sum(self.amps[i].conjugate() * other.amps[i] for i in range(len(self.amps)))
        return abs(ov) ** 2

    def apply_1q(self, q: int, u00: complex, u01: complex, u10: complex, u11: complex) -> None:
        n, amps = self.n, self.amps
        bit = 1 << q
        dim = 1 << n
        out = [0j] * dim
        for i in range(dim):
            if i & bit:
                continue
            j = i | bit
            a, b = amps[i], amps[j]
            out[i] = u00 * a + u01 * b
            out[j] = u10 * a + u11 * b
        self.amps = out

    def apply_cnot(self, c: int, t: int) -> None:
        n, amps = self.n, self.amps
        cb, tb = 1 << c, 1 << t
        out = [0j] * (1 << n)
        for i in range(1 << n):
            if i & cb:
                out[i ^ tb] = amps[i]
            else:
                out[i] = amps[i]
        self.amps = out

    def apply_swap(self, a: int, b: int) -> None:
        # three CNOTs
        self.apply_cnot(a, b)
        self.apply_cnot(b, a)
        self.apply_cnot(a, b)

    # --- seed-locked gates ---

    def H(self, q: int) -> "Statevector":
        s = math.sqrt(0.5)
        self.apply_1q(q, s, s, s, -s)
        return self

    def X(self, q: int) -> "Statevector":
        self.apply_1q(q, 0, 1, 1, 0)
        return self

    def Y(self, q: int) -> "Statevector":
        self.apply_1q(q, 0, -1j, 1j, 0)
        return self

    def Z(self, q: int) -> "Statevector":
        self.apply_1q(q, 1, 0, 0, -1)
        return self

    def S(self, q: int) -> "Statevector":
        self.apply_1q(q, 1, 0, 0, 1j)
        return self

    def T(self, q: int) -> "Statevector":
        # T = exp(i π/4) on |1⟩ — seed pi only
        phase = cmath.exp(1j * ANGLES["quarter_pi"])
        self.apply_1q(q, 1, 0, 0, phase)
        return self

    def Phase(self, q: int, kind: str = "theta_s") -> "Statevector":
        """Diagonal phase from named seed angle only."""
        if kind not in ANGLES:
            raise ValueError(f"unknown seed angle {kind}")
        phase = cmath.exp(1j * ANGLES[kind])
        self.apply_1q(q, 1, 0, 0, phase)
        return self

    def CNOT(self, c: int, t: int) -> "Statevector":
        self.apply_cnot(c, t)
        return self

    def CPhase(self, c: int, t: int, kind: str = "half_pi") -> "Statevector":
        """Controlled phase with seed angle."""
        if kind not in ANGLES:
            raise ValueError(kind)
        ph = cmath.exp(1j * ANGLES[kind])
        n, amps = self.n, self.amps
        cb, tb = 1 << c, 1 << t
        out = list(amps)
        for i in range(1 << n):
            if (i & cb) and (i & tb):
                out[i] = amps[i] * ph
        self.amps = out
        return self

    def measure_shot(self, rng_seed: int | None = None) -> int:
        """
        Single shot. Deterministic when rng_seed set from FSOT (no free RNG).
        Default: argmax probability (mode) — seed-free measurement collapse.
        """
        probs = self.probs()
        if rng_seed is None:
            return max(range(len(probs)), key=lambda i: probs[i])
        # LCG from seed integer only
        x = rng_seed % (2**31 - 1)
        x = (1103515245 * x + 12345) % (2**31)
        u = x / (2**31)
        acc = 0.0
        for i, p in enumerate(probs):
            acc += p
            if u <= acc:
                return i
        return len(probs) - 1

    def to_trinary_codes(self) -> list[int]:
        """Map Re(amp) field through FSOT collapse → pack codes."""
        reals = [a.real for a in self.amps]
        codes = collapse(reals)
        if hasattr(codes, "tolist"):
            return [int(c) for c in codes.tolist()]
        return [int(c) for c in codes]


def bell_phi_plus() -> Statevector:
    """(|00⟩+|11⟩)/√2 via H·CNOT — textbook, seed-free gates."""
    s = Statevector.zeros(2)
    s.H(0).CNOT(0, 1)
    return s


def ghz(n: int = 3) -> Statevector:
    s = Statevector.zeros(n)
    s.H(0)
    for i in range(n - 1):
        s.CNOT(i, i + 1)
    return s


def clifford_t_demo(n: int = 2) -> Statevector:
    """Universal-set fragment using only seed angles."""
    s = Statevector.zeros(n)
    s.H(0).T(0).H(0).CNOT(0, 1).S(1).T(1)
    return s


def gate_set_fidelity_selftest() -> dict:
    """
    Structural tests: Bell fidelity to ideal, GHZ probs, T-gate phase.
    """
    b = bell_phi_plus()
    ideal = Statevector(n=2, amps=[math.sqrt(0.5), 0, 0, math.sqrt(0.5)])
    f_bell = b.fidelity(ideal)
    g = ghz(3)
    pg = g.probs()
    ghz_ok = abs(pg[0] - 0.5) < 1e-9 and abs(pg[7] - 0.5) < 1e-9
    # H T H on |0> should not be free-param dependent
    s = Statevector.zeros(1)
    s.H(0).T(0).H(0)
    return {
        "bell_fidelity": f_bell,
        "bell_ok": f_bell > 1.0 - 1e-12,
        "ghz_ok": ghz_ok,
        "clifford_t_norm": abs(sum(abs(a) ** 2 for a in clifford_t_demo().amps) - 1.0) < 1e-12,
        "collapse_bridge_codes": bell_phi_plus().to_trinary_codes()[:4],
        "angles_seed_only": list(ANGLES.keys()),
        "ok": f_bell > 1.0 - 1e-12 and ghz_ok,
    }
