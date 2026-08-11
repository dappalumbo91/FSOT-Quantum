"""Circuit runner on TritRegister — FSOT gates only."""

from __future__ import annotations

from dataclasses import dataclass, field

from fsot_quantum.domains import DOMAIN_COMPUTE
from fsot_quantum.gates import Gate, GateName, apply_gate, gate_domain
from fsot_quantum.measure import measure_register
from fsot_quantum.register import TritRegister


@dataclass
class Circuit:
    n: int
    gates: list[Gate] = field(default_factory=list)
    domain: str = DOMAIN_COMPUTE

    def add(self, name: GateName | str, *wires: int) -> "Circuit":
        gname = GateName(name) if not isinstance(name, GateName) else name
        for w in wires:
            if not (0 <= w < self.n):
                raise IndexError(w)
        self.gates.append(Gate(gname, tuple(wires)))
        return self

    def x(self, i: int) -> "Circuit":
        return self.add(GateName.X, i)

    def h(self, i: int) -> "Circuit":
        return self.add(GateName.H, i)

    def z(self, i: int) -> "Circuit":
        return self.add(GateName.Z, i)

    def cx(self, c: int, t: int) -> "Circuit":
        return self.add(GateName.CX, c, t)

    def measure(self, *wires: int) -> "Circuit":
        if not wires:
            for i in range(self.n):
                self.add(GateName.MEASURE, i)
        else:
            for w in wires:
                self.add(GateName.MEASURE, w)
        return self


def run_circuit(reg: TritRegister, circuit: Circuit, *, domain: str | None = None) -> TritRegister:
    out = reg.copy()
    if domain:
        out.domain = domain
    base = out.domain or circuit.domain
    pending: list[int] = []
    for g in circuit.gates:
        if g.name == GateName.MEASURE:
            pending.extend(g.wires)
            continue
        if pending:
            out = measure_register(out, wires=sorted(set(pending)), domain=base)
            pending = []
        use = gate_domain(g.name)
        out.spins = apply_gate(out.spins, g, domain=use)
    if pending:
        out = measure_register(out, wires=sorted(set(pending)), domain=base)
    return out


def bell_analog() -> Circuit:
    return Circuit(2).h(0).cx(0, 1).measure(0, 1)
