"""
FSOT trinary quantum circuits.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from fsot_quantum.domains import DOMAIN_COMPUTE
from fsot_quantum.gates import Gate, GateName, apply_gate, default_domain_for_gate
from fsot_quantum.measure import measure_register
from fsot_quantum.qubit import TritRegister


@dataclass
class Circuit:
    n: int
    gates: list[Gate] = field(default_factory=list)
    domain: str = DOMAIN_COMPUTE

    def add(self, name: GateName | str, *wires: int) -> "Circuit":
        gname = GateName(name) if not isinstance(name, GateName) else name
        for w in wires:
            if w < 0 or w >= self.n:
                raise IndexError(f"wire {w} out of range for n={self.n}")
        self.gates.append(Gate(gname, tuple(wires)))
        return self

    # fluent helpers
    def x(self, i: int) -> "Circuit":
        return self.add(GateName.X, i)

    def h(self, i: int) -> "Circuit":
        return self.add(GateName.H, i)

    def z(self, i: int) -> "Circuit":
        return self.add(GateName.Z, i)

    def s(self, i: int) -> "Circuit":
        return self.add(GateName.S, i)

    def cx(self, c: int, t: int) -> "Circuit":
        return self.add(GateName.CX, c, t)

    def cz(self, c: int, t: int) -> "Circuit":
        return self.add(GateName.CZ, c, t)

    def ccx(self, c1: int, c2: int, t: int) -> "Circuit":
        return self.add(GateName.CCX, c1, c2, t)

    def measure(self, *wires: int) -> "Circuit":
        if not wires:
            for i in range(self.n):
                self.add(GateName.MEASURE, i)
        else:
            for w in wires:
                self.add(GateName.MEASURE, w)
        return self


def run_circuit(
    reg: TritRegister,
    circuit: Circuit,
    *,
    domain: str | None = None,
) -> TritRegister:
    """Execute circuit on a copy of the register."""
    out = reg.copy()
    if domain:
        out.domain = domain
    base_domain = out.domain or circuit.domain

    pending_measure: list[int] = []
    for g in circuit.gates:
        if g.name == GateName.MEASURE:
            pending_measure.extend(g.wires)
            continue
        # flush measures before unitary-like ops if interleaved
        if pending_measure:
            out = measure_register(out, wires=sorted(set(pending_measure)), domain=base_domain)
            pending_measure = []
        gdom = default_domain_for_gate(g.name)
        # observer-ish gates use spin law; others use compute domain
        use_dom = gdom if g.name in (GateName.H, GateName.Z, GateName.S) else base_domain
        out.spins = apply_gate(out.spins, g, domain=use_dom)

    if pending_measure:
        out = measure_register(out, wires=sorted(set(pending_measure)), domain=base_domain)
    return out


def bell_analog_circuit() -> Circuit:
    """
    FSOT Bell-analog on 2 spins:
      H on 0, CX 0→1
    Produces correlated trinary pair under measure.
    """
    return Circuit(2).h(0).cx(0, 1).measure(0, 1)


def deutsch_analog() -> Circuit:
    """
    Minimal oracle-style 2-wire pattern for pathway demo:
      H0, H1, CX, H0, measure
    """
    return Circuit(2).h(0).h(1).cx(0, 1).h(0).measure(0, 1)
