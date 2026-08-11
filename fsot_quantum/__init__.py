"""
FSOT-Quantum — Fluid Spacetime Omni-Theory alternative quantum computing.

Theory authority: FSOT-2.1-Lean (pin D1D38A).
Trinary spins: −1 = spin down, 0 = superposition, +1 = spin up.
Zero free parameters. No ad-hoc coefficients.
"""

from fsot_quantum.seeds import SEEDS, COLLAPSE_THRESHOLD, PIN_EXPECTED
from fsot_quantum.scalar import compute_scalar, domain_scalar
from fsot_quantum.domains import DOMAINS, DomainConfig
from fsot_quantum.trinary import (
    Spin,
    SPIN_DOWN,
    SUPERPOSED,
    SPIN_UP,
    collapse_scalar,
    code_to_signed,
    signed_to_code,
    pack_u64,
    unpack_u64,
)
from fsot_quantum.qubit import TritRegister, continuous_field_from_spins
from fsot_quantum.gates import Gate, apply_gate, GATE_TABLE
from fsot_quantum.circuit import Circuit, run_circuit
from fsot_quantum.measure import measure_register, measure_spin

__all__ = [
    "SEEDS",
    "COLLAPSE_THRESHOLD",
    "PIN_EXPECTED",
    "compute_scalar",
    "domain_scalar",
    "DOMAINS",
    "DomainConfig",
    "Spin",
    "SPIN_DOWN",
    "SUPERPOSED",
    "SPIN_UP",
    "collapse_scalar",
    "code_to_signed",
    "signed_to_code",
    "pack_u64",
    "unpack_u64",
    "TritRegister",
    "continuous_field_from_spins",
    "Gate",
    "apply_gate",
    "GATE_TABLE",
    "Circuit",
    "run_circuit",
    "measure_register",
    "measure_spin",
]

__version__ = "0.1.0"
