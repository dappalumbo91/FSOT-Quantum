"""
FSOT trinary quantum gates — derived from seed ops only.

No complex matrices. No free-parameter angles.
Gate set is the FSOT trit machine model + quantum domain routing.

Signed spins: −1 down, 0 superposed, +1 up.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW
from fsot_quantum.scalar import domain_scalar
from fsot_quantum.seeds import SEEDS
from fsot_quantum.trinary import (
    SPIN_DOWN,
    SPIN_UP,
    SUPERPOSED,
    consensus,
    neg,
    pair,
    sum_sat,
)


class GateName(str, Enum):
    I = "I"  # identity
    X = "X"  # polarity flip (neg)
    Z = "Z"  # sign mark via pair with domain phase class
    H = "H"  # superpose / resolve (Hadamard-analog)
    S = "S"  # phase-class rotate by domain delta_psi class
    CX = "CX"  # controlled-X (CNOT-analog)
    CZ = "CZ"  # controlled-Z
    CCX = "CCX"  # Toffoli-analog (double control)
    CONSENSUS = "CONSENSUS"  # two-wire agreement
    PAIR = "PAIR"  # two-wire product into target
    MEASURE = "MEASURE"  # collapse site (see measure.py)


@dataclass(frozen=True)
class Gate:
    name: GateName
    wires: tuple[int, ...]  # target last for multi-wire gates


def _phase_class_from_domain(domain: str) -> int:
    """
    Domain phase → trinary class without free parameters.
    Uses sign of domain scalar S and |S| vs collapse-adjacent C_eff.
    """
    s = domain_scalar(domain)
    if s > SEEDS.c_eff:
        return int(SPIN_UP)
    if s < -SEEDS.c_eff:
        return int(SPIN_DOWN)
    return int(SUPERPOSED)


def _h_analog(t: int, domain: str) -> int:
    """
    Hadamard-analog (FSOT fluid):
      ±1 → 0   (pole bleeds into superposed continuum)
      0  → sign(S_domain) mapped to ±1  (observer/compute resolve)

    Quantum_Mechanics S > 0 → superposed resolves UP (emergence).
    Quantum_Computing S < 0 → superposed resolves DOWN (compute damp).
    """
    t = int(t)
    if t != 0:
        return int(SUPERPOSED)
    s = domain_scalar(domain)
    if s > 0:
        return int(SPIN_UP)
    if s < 0:
        return int(SPIN_DOWN)
    return int(SUPERPOSED)


def _z_analog(t: int, domain: str) -> int:
    """
    Z-analog: pair spin with domain phase class.
    Superposed stays superposed (pair with anything gives 0 if t=0).
    """
    return pair(t, _phase_class_from_domain(domain))


def _s_phase(t: int, domain: str) -> int:
    """
    S-gate analog: sum_sat with phase class (local field inject).
    """
    return sum_sat(t, _phase_class_from_domain(domain))


def apply_unary(name: GateName, t: int, domain: str) -> int:
    t = int(t)
    if name == GateName.I:
        return t
    if name == GateName.X:
        return neg(t)
    if name == GateName.Z:
        return _z_analog(t, domain)
    if name == GateName.H:
        return _h_analog(t, domain)
    if name == GateName.S:
        return _s_phase(t, domain)
    raise ValueError(f"not a unary gate: {name}")


def apply_cx(control: int, target: int) -> int:
    """
    CNOT-analog:
      control = +1 → flip target (neg)
      control = −1 → leave target
      control =  0 → force superposed (decoherence / open valve)
    """
    c, t = int(control), int(target)
    if c == 0:
        return int(SUPERPOSED)
    if c > 0:
        return neg(t)
    return t


def apply_cz(control: int, target: int, domain: str) -> int:
    """CZ-analog: if control up, apply Z to target; if super, super; if down, leave."""
    c, t = int(control), int(target)
    if c == 0:
        return int(SUPERPOSED)
    if c > 0:
        return _z_analog(t, domain)
    return t


def apply_ccx(c1: int, c2: int, target: int) -> int:
    """Toffoli-analog: flip target only if both controls are UP."""
    if int(c1) == 1 and int(c2) == 1:
        return neg(target)
    if int(c1) == 0 or int(c2) == 0:
        return int(SUPERPOSED)
    return int(target)


def apply_gate(spins: list[int], gate: Gate, domain: str = DOMAIN_COMPUTE) -> list[int]:
    """Apply one gate in-place-copy on a spin list."""
    out = list(spins)
    name = gate.name
    w = gate.wires
    if name in (GateName.I, GateName.X, GateName.Z, GateName.H, GateName.S):
        if len(w) != 1:
            raise ValueError(f"{name} needs 1 wire")
        i = w[0]
        out[i] = apply_unary(name, out[i], domain)
        return out
    if name == GateName.CX:
        if len(w) != 2:
            raise ValueError("CX needs (control, target)")
        c, t = w
        out[t] = apply_cx(out[c], out[t])
        return out
    if name == GateName.CZ:
        if len(w) != 2:
            raise ValueError("CZ needs (control, target)")
        c, t = w
        out[t] = apply_cz(out[c], out[t], domain)
        return out
    if name == GateName.CCX:
        if len(w) != 3:
            raise ValueError("CCX needs (c1, c2, target)")
        c1, c2, t = w
        out[t] = apply_ccx(out[c1], out[c2], out[t])
        return out
    if name == GateName.CONSENSUS:
        if len(w) != 2:
            raise ValueError("CONSENSUS needs 2 wires; writes wire[1]")
        a, b = w
        out[b] = consensus(out[a], out[b])
        return out
    if name == GateName.PAIR:
        if len(w) != 2:
            raise ValueError("PAIR needs 2 wires; writes wire[1]")
        a, b = w
        out[b] = pair(out[a], out[b])
        return out
    if name == GateName.MEASURE:
        # deferred to measure.py path; identity here if mis-routed
        return out
    raise ValueError(f"unknown gate {name}")


# Human-readable table for docs / verify
GATE_TABLE: dict[str, str] = {
    "I": "identity",
    "X": "neg(t) polarity flip",
    "Z": "pair(t, phase_class(domain))",
    "H": "±1→0; 0→sign(S_domain)",
    "S": "sum_sat(t, phase_class(domain))",
    "CX": "control+1 flip; control0 super; control−1 hold",
    "CZ": "control+1 Z; control0 super; control−1 hold",
    "CCX": "both controls +1 → flip target",
    "CONSENSUS": "agreement gate into target",
    "PAIR": "product into target",
}


def default_domain_for_gate(name: GateName) -> str:
    """Spin-law domain for observer-ish gates; compute substrate otherwise."""
    if name in (GateName.H, GateName.Z, GateName.S, GateName.MEASURE):
        return DOMAIN_SPIN_LAW
    return DOMAIN_COMPUTE
