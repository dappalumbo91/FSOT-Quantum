"""
FSOT-Quantum — Quantum_Mechanics / Quantum_Computing domain fold.

Implementation authority: FSOT-GPU fsot_lib (this repo vendors it).
Theory authority: FSOT-2.1-Lean pin D1D38A.

Spins (signed, same as Lean/Zig/GPU):
  -1 = spin down, 0 = superposed, +1 = spin up
Pack codes (fsot_lib): 0=down, 1=super, 2=up
"""

from fsot_lib.seeds import SEEDS, COLLAPSE_THRESHOLD
from fsot_lib.scalar import compute_scalar
from fsot_lib.trinary import collapse, pack_u64, unpack_u64, trit_similarity
from fsot_lib.coherence import coherence_norm, position_coherence
from fsot_lib.consensus import consensus_aggregate, apply_phase_rotation

from fsot_quantum.domains import DOMAINS, domain_scalar, DOMAIN_SPIN_LAW, DOMAIN_COMPUTE
from fsot_quantum.register import TritRegister
from fsot_quantum.gates import Gate, GateName, apply_gate
from fsot_quantum.circuit import Circuit, run_circuit
from fsot_quantum.engine import QuantumEngine, run_engine_smoke
from fsot_quantum.measure import measure_register

__all__ = [
    "SEEDS",
    "COLLAPSE_THRESHOLD",
    "compute_scalar",
    "collapse",
    "pack_u64",
    "unpack_u64",
    "trit_similarity",
    "coherence_norm",
    "position_coherence",
    "consensus_aggregate",
    "apply_phase_rotation",
    "DOMAINS",
    "domain_scalar",
    "DOMAIN_SPIN_LAW",
    "DOMAIN_COMPUTE",
    "TritRegister",
    "Gate",
    "GateName",
    "apply_gate",
    "Circuit",
    "run_circuit",
    "QuantumEngine",
    "run_engine_smoke",
    "measure_register",
]

__version__ = "0.2.0"
