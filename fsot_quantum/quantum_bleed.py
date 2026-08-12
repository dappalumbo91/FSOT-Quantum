"""
Quantum-sector fluid bleed — twin of FSOT-2.1-Lean vendor/fsot_complex_interaction.py

Not every quantum interaction lives at one D_eff (6 vs 11).
Sectors talk through seed-locked coupling:

  κ_ij = A_bleed · POOF · |S_i| |S_j| / (1 + |D_i − D_j|/25)

  dS_i/dt = Σ_j κ_ij (S_j − S_i) − γ (S_i − S_i^eq)

  I_ab = |S_a − S_b| / (|S_a| + |S_b|)

  O = O_seed · (1 + POOF · SUCTION · (I_plus − I_minus))

Zero free parameters. Topology is the physics skeleton (who talks to whom).
Authority: FSOT-2.1-Lean COMPLEX_SYSTEM_DERIVATION.md + pin D1D38A.
"""

from __future__ import annotations

import math
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import DOMAINS, domain_scalar


# Structural quantum-sector graph — not a fit.
# Same idea as Lean GR/EW/QCD/QED/flavor skeleton, for this granular fold.
QUANTUM_NODES: dict[str, dict[str, Any]] = {
    "QM": {"domain": "Quantum_Mechanics", "role": "measurement_spin_law"},
    "QC": {"domain": "Quantum_Computing", "role": "compute_substrate"},
    "QO": {"domain": "Quantum_Optics", "role": "phase_optics"},
    "PART": {"domain": "Particle_Physics", "role": "micro_flavor"},
    "ATOM": {"domain": "Atomic_Physics", "role": "atomic_bridge"},
    "HEP": {"domain": "High_Energy_Physics", "role": "ew_higgs_class"},
    "CHEM": {"domain": "Chemistry", "role": "bond_observables"},
    "MOL": {"domain": "Molecular_Chemistry", "role": "molecular_jobs"},
    "CM": {"domain": "Condensed_Matter", "role": "packing_graphs"},
    "QG": {"domain": "Quantum_Gravity", "role": "deep_residual"},
}

QUANTUM_EDGES: tuple[tuple[str, str], ...] = (
    ("QM", "QC"),
    ("QM", "QO"),
    ("QM", "PART"),
    ("QM", "ATOM"),
    ("QC", "QO"),
    ("QC", "CM"),
    ("QC", "CHEM"),
    ("QC", "MOL"),
    ("PART", "HEP"),
    ("PART", "ATOM"),
    ("ATOM", "CHEM"),
    ("CHEM", "MOL"),
    ("CM", "CHEM"),
    ("QG", "QM"),
    ("QG", "QC"),
)


def _D(node: str) -> float:
    return float(DOMAINS[QUANTUM_NODES[node]["domain"]].D_eff)


def _S_eq(node: str) -> float:
    return float(domain_scalar(QUANTUM_NODES[node]["domain"]))


def coupling_kappa(i: str, j: str) -> float:
    s = SEEDS
    Si, Sj = abs(_S_eq(i)), abs(_S_eq(j))
    dist = abs(_D(i) - _D(j)) / 25.0
    return float(s.a_bleed) * float(s.poof) * Si * Sj / (1.0 + dist)


def interface_index(Sa: float, Sb: float) -> float:
    den = abs(Sa) + abs(Sb)
    if den <= 1e-30:
        return 0.0
    return abs(Sa - Sb) / den


def yin_yang_fraction() -> float:
    p, u = float(SEEDS.poof), float(SEEDS.suction)
    return p / max(p + u, 1e-30)


def coupled_equilibrium() -> dict[str, Any]:
    """Seed-rate relaxation. dt = POOF·SUCTION; steps = round(1/POOF)."""
    s = SEEDS
    names = list(QUANTUM_NODES.keys())
    seq = [_S_eq(n) for n in names]
    S = list(seq)
    idx = {n: k for k, n in enumerate(names)}
    kap: dict[tuple[int, int], float] = {}
    for a, b in QUANTUM_EDGES:
        ia, ib = idx[a], idx[b]
        k = coupling_kappa(a, b)
        kap[(ia, ib)] = k
        kap[(ib, ia)] = k

    gamma = abs(float(s.chaos)) + float(s.psi_con) * float(s.poof)
    dt = float(s.poof) * float(s.suction)
    steps = max(1, int(round(1.0 / float(s.poof))))

    for _ in range(steps):
        nxt = list(S)
        for i, name in enumerate(names):
            acc = 0.0
            for j, _other in enumerate(names):
                if i == j:
                    continue
                k = kap.get((i, j), 0.0)
                if k == 0.0:
                    continue
                acc += k * (S[j] - S[i])
            nxt[i] = S[i] + dt * (acc - gamma * (S[i] - seq[i]))
        S = nxt

    coupled = {n: S[i] for i, n in enumerate(names)}
    bare = {n: seq[i] for i, n in enumerate(names)}
    ifaces = {}
    for a, b in QUANTUM_EDGES:
        ifaces[f"{a}-{b}"] = {
            "kappa": coupling_kappa(a, b),
            "I_bare": interface_index(bare[a], bare[b]),
            "I_coupled": interface_index(coupled[a], coupled[b]),
            "D": [_D(a), _D(b)],
        }
    return {
        "bare_S": bare,
        "coupled_S": coupled,
        "interfaces": ifaces,
        "yin_yang": yin_yang_fraction(),
        "gamma": gamma,
        "dt": dt,
        "steps": steps,
        "nodes": {
            n: {
                "domain": QUANTUM_NODES[n]["domain"],
                "role": QUANTUM_NODES[n]["role"],
                "D_eff": _D(n),
                "S_eq": bare[n],
                "S_coupled": coupled[n],
            }
            for n in names
        },
    }


def seed_modulation(I_plus: float, I_minus: float) -> float:
    """O/O_seed = 1 + POOF·SUCTION·(I+ − I−). Lean complex-system note."""
    return 1.0 + float(SEEDS.poof) * float(SEEDS.suction) * (I_plus - I_minus)


def qc_job_modulation(eq: dict[str, Any]) -> dict[str, float]:
    """
    How much the compute job 'waves' toward neighbors.
    I+ = QC–CM (packing / graphs), I− = QC–QM (measurement back-action).
    """
    ifaces = eq["interfaces"]
    i_pack = ifaces["QC-CM"]["I_coupled"]
    i_meas = ifaces["QM-QC"]["I_coupled"]
    return {
        "mod": seed_modulation(i_pack, i_meas),
        "I_QC_CM": i_pack,
        "I_QM_QC": i_meas,
    }
