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
    """Vendor §5 — all 35 pin domains. No extras, no drops."""
    s = SEEDS
    gp = s.gamma / s.phi
    ep = s.e / s.pi
    lnpi_e = math.log(s.pi) / s.e
    pi_e = s.pi / s.e
    ab_s2 = s.a_bleed / math.sqrt(2.0)
    s2_e = math.sqrt(2.0) / s.e
    lnphi_s2 = math.log(s.phi) / math.sqrt(2.0)
    alpha_phi = s.alpha / s.phi
    chaos_half = s.chaos / 2.0
    pi2_phi = (s.pi ** 2) / s.phi
    pi2_e = (s.pi ** 2) / s.e
    inv_phi2 = 1.0 / (s.phi ** 2)
    c_cosm = 1.0 / (s.phi * 10.0)
    p_base = s.gamma / s.e
    rows = [
        DomainConfig("Particle_Physics", 5, 0, 1.0, 1.0, True, gp),
        DomainConfig("Quantum_Mechanics", 6, 0, 1.0, 1.0, True, gp),
        DomainConfig("Atomic_Physics", 7, 0, 0.85, 1.0, True, ep),
        DomainConfig("Physical_Chemistry", 8, 0, 0.5, 1.0, True, ep),
        DomainConfig("Chemistry", 8, 0, 0.6, 1.0, True, ep),
        DomainConfig("Electromagnetism", 9, 0, 0.7, 1.0, True, ep),
        DomainConfig("Molecular_Chemistry", 9, 0, 0.5, 1.0, True, lnpi_e),
        DomainConfig("Optics", 10, 0, 0.6, 1.0, True, pi_e),
        DomainConfig("Acoustics", 10, 0, 0.3, 1.0, True, ab_s2),
        DomainConfig("Quantum_Computing", 11, 0, 0.5, 1.0, False, s2_e),
        DomainConfig("Quantum_Optics", 11, 0, 0.6, 1.0, True, pi_e),
        DomainConfig("Biology", 12, 0, 0.08, 1.0, False, lnphi_s2),
        DomainConfig("Thermodynamics", 15, 1, 0.9, 1.0, True, p_base),
        DomainConfig("Biochemistry", 13, 1, 0.35, 1.0, True, lnphi_s2),
        DomainConfig("Neuroscience", 14, 1, 0.7, 1.0, True, s.c_factor),
        DomainConfig("Condensed_Matter", 14, 0, 0.5, 1.0, True, s.a_bleed / s.e),
        DomainConfig("Fluid_Dynamics", 15, 1, 0.9, 1.0, False, s.a_bleed / s.phi),
        DomainConfig("Nuclear_Physics", 15, 1, 1.0, 1.0, True, alpha_phi),
        DomainConfig("Ecology", 15, 1, 0.2, 1.0, False, math.log(s.phi) / s.phi),
        DomainConfig("Meteorology", 16, 2, 0.8, 1.0, False, s.chaos),
        DomainConfig("Materials_Science", 10, 0, 0.5, 1.0, True, s.a_in / s.e),
        DomainConfig("Psychology", 16, 1, 1.15, 1.0, True, p_base),
        DomainConfig("Atmospheric_Physics", 17, 2, 0.8, 1.0, False, s.chaos),
        DomainConfig("Oceanography", 17, 1, 0.7, 1.0, False, s.a_in / s.phi),
        DomainConfig("Seismology", 18, 2, 1.2, 1.0, False, chaos_half),
        DomainConfig("Sociology", 18, 3, 1.5, 1.0, True, s.gamma / math.log(s.pi)),
        DomainConfig("High_Energy_Physics", 7, 1, 0.95, 1.0, True, s.alpha / math.sqrt(2.0)),
        DomainConfig("Geophysics", 19, 2, 1.0, 1.0, False, s.chaos),
        DomainConfig("Astronomy", 20, 1, 1.0, 1.0, True, pi2_phi),
        DomainConfig("Economics", 20, 3, 1.5, 1.0, True, s.gamma / math.log(s.pi)),
        DomainConfig("Planetary_Science", 21, 1, 0.9, 1.0, True, pi2_phi),
        DomainConfig("Quantum_Gravity", 22, 0, 1.0, 1.0, False, inv_phi2),
        DomainConfig("Particle_Astrophysics", 24, 0, 0.8, 1.0, False, pi2_e),
        DomainConfig("Astrophysics", 24, 1, 1.0, 1.0, True, pi2_phi),
        DomainConfig("Cosmology", 25, 0, 1.0, 1.0, False, c_cosm),
    ]
    return {d.name: d for d in rows}


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
