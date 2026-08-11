"""
Preregistered domain folds used by the quantum pathway.

Source: vendor/fsot_compute.py DOMAINS table (pin D1D38A).
Quantum pathway uses:
  - Quantum_Mechanics  (D_eff=6,  observed=True)  — residual / spin law
  - Quantum_Computing  (D_eff=11, observed=False) — bare compute substrate
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from fsot_quantum.seeds import SEEDS


@dataclass(frozen=True)
class DomainConfig:
    name: str
    D_eff: int
    hits: int
    delta_psi: float
    delta_theta: float
    observed: bool
    C: float  # domain interpretation constant (seed-derived)


def _build_domains() -> dict[str, DomainConfig]:
    s = SEEDS
    gp = s.gamma / s.phi
    s2_e = math.sqrt(2.0) / s.e
    return {
        "Particle_Physics": DomainConfig("Particle_Physics", 5, 0, 1.0, 1.0, True, gp),
        "Quantum_Mechanics": DomainConfig("Quantum_Mechanics", 6, 0, 1.0, 1.0, True, gp),
        "Quantum_Computing": DomainConfig(
            "Quantum_Computing", 11, 0, 0.5, 1.0, False, s2_e
        ),
        "Quantum_Optics": DomainConfig(
            "Quantum_Optics", 11, 0, 0.6, 1.0, True, s.pi / s.e
        ),
        "Quantum_Gravity": DomainConfig(
            "Quantum_Gravity", 22, 0, 1.0, 1.0, False, 1.0 / (s.phi**2)
        ),
        "Cosmology": DomainConfig(
            "Cosmology", 25, 0, 1.0, 1.0, False, s.c_cosm
        ),
    }


DOMAINS = _build_domains()

# Pathway defaults
DOMAIN_SPIN_LAW = "Quantum_Mechanics"
DOMAIN_COMPUTE = "Quantum_Computing"
