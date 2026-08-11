"""
Preregistered quantum domain folds — from vendor/fsot_compute.py DOMAINS.

Uses fsot_lib.scalar.compute_scalar (FSOT-GPU owned) with Lean table routes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from fsot_lib.seeds import SEEDS
from fsot_lib.scalar import compute_scalar


@dataclass(frozen=True)
class DomainConfig:
    name: str
    D_eff: int
    hits: int
    delta_psi: float
    delta_theta: float
    observed: bool
    C: float


def _build() -> dict[str, DomainConfig]:
    s = SEEDS
    gp = s.gamma / s.phi
    s2_e = math.sqrt(2.0) / s.e
    return {
        "Quantum_Mechanics": DomainConfig(
            "Quantum_Mechanics", 6, 0, 1.0, 1.0, True, gp
        ),
        "Quantum_Computing": DomainConfig(
            "Quantum_Computing", 11, 0, 0.5, 1.0, False, s2_e
        ),
        "Quantum_Optics": DomainConfig(
            "Quantum_Optics", 11, 0, 0.6, 1.0, True, s.pi / s.e
        ),
        "Particle_Physics": DomainConfig(
            "Particle_Physics", 5, 0, 1.0, 1.0, True, gp
        ),
        "Quantum_Gravity": DomainConfig(
            "Quantum_Gravity", 22, 0, 1.0, 1.0, False, 1.0 / (s.phi**2)
        ),
    }


DOMAINS = _build()
DOMAIN_SPIN_LAW = "Quantum_Mechanics"
DOMAIN_COMPUTE = "Quantum_Computing"


def domain_scalar(name: str) -> float:
    d = DOMAINS[name]
    return float(
        compute_scalar(
            N=1.0,
            P=1.0,
            D_eff=float(d.D_eff),
            delta_psi=float(d.delta_psi),
            recent_hits=float(d.hits),
            observed=d.observed,
            delta_theta=float(d.delta_theta),
            rho=1.0,
            scale=1.0,
            amplitude=1.0,
            trend_bias=0.0,
        )
    )
