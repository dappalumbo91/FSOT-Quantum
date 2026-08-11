"""
Quantum pathway gates — built only from FSOT trit ops + domain S.

Uses fsot_lib seeds/scalar routing. No complex matrices. No free angles.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW, domain_scalar


class GateName(str, Enum):
    I = "I"
    X = "X"  # polarity flip
    Z = "Z"
    H = "H"
    S = "S"
    CX = "CX"
    CZ = "CZ"
    CCX = "CCX"
    CONSENSUS = "CONSENSUS"
    PAIR = "PAIR"
    MEASURE = "MEASURE"


@dataclass(frozen=True)
class Gate:
    name: GateName
    wires: tuple[int, ...]


def neg(t: int) -> int:
    return -int(t)


def pair(a: int, b: int) -> int:
    return int(a) * int(b)


def consensus(a: int, b: int) -> int:
    a, b = int(a), int(b)
    return a if a == b else 0


def sum_sat(a: int, b: int) -> int:
    s = int(a) + int(b)
    if s > 1:
        return 1
    if s < -1:
        return -1
    return s


def phase_class(domain: str) -> int:
    """sign / magnitude of domain S → trit class (seed law only)."""
    s = domain_scalar(domain)
    if s > SEEDS.c_eff:
        return 1
    if s < -SEEDS.c_eff:
        return -1
    return 0


def h_analog(t: int, domain: str) -> int:
    """±1 → superposed; 0 → sign(S_domain)."""
    t = int(t)
    if t != 0:
        return 0
    s = domain_scalar(domain)
    if s > 0:
        return 1
    if s < 0:
        return -1
    return 0


def apply_unary(name: GateName, t: int, domain: str) -> int:
    t = int(t)
    if name == GateName.I:
        return t
    if name == GateName.X:
        return neg(t)
    if name == GateName.Z:
        return pair(t, phase_class(domain))
    if name == GateName.H:
        return h_analog(t, domain)
    if name == GateName.S:
        return sum_sat(t, phase_class(domain))
    raise ValueError(name)


def apply_cx(c: int, t: int) -> int:
    c, t = int(c), int(t)
    if c == 0:
        return 0
    if c > 0:
        return neg(t)
    return t


def apply_cz(c: int, t: int, domain: str) -> int:
    c, t = int(c), int(t)
    if c == 0:
        return 0
    if c > 0:
        return pair(t, phase_class(domain))
    return t


def apply_ccx(c1: int, c2: int, t: int) -> int:
    if int(c1) == 1 and int(c2) == 1:
        return neg(t)
    if int(c1) == 0 or int(c2) == 0:
        return 0
    return int(t)


def apply_gate(spins: list[int], gate: Gate, domain: str = DOMAIN_COMPUTE) -> list[int]:
    out = list(spins)
    name, w = gate.name, gate.wires
    if name in (GateName.I, GateName.X, GateName.Z, GateName.H, GateName.S):
        i = w[0]
        out[i] = apply_unary(name, out[i], domain)
        return out
    if name == GateName.CX:
        c, t = w
        out[t] = apply_cx(out[c], out[t])
        return out
    if name == GateName.CZ:
        c, t = w
        out[t] = apply_cz(out[c], out[t], domain)
        return out
    if name == GateName.CCX:
        c1, c2, t = w
        out[t] = apply_ccx(out[c1], out[c2], out[t])
        return out
    if name == GateName.CONSENSUS:
        a, b = w
        out[b] = consensus(out[a], out[b])
        return out
    if name == GateName.PAIR:
        a, b = w
        out[b] = pair(out[a], out[b])
        return out
    if name == GateName.MEASURE:
        return out
    raise ValueError(name)


def gate_domain(name: GateName) -> str:
    if name in (GateName.H, GateName.Z, GateName.S, GateName.MEASURE):
        return DOMAIN_SPIN_LAW
    return DOMAIN_COMPUTE
