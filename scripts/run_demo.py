#!/usr/bin/env python3
"""Demo: quantum pathway on fsot_lib (FSOT-GPU implementation)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD
from fsot_quantum.circuit import Circuit, bell_analog
from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW, domain_scalar
from fsot_quantum.engine import QuantumEngine
from fsot_quantum.register import TritRegister


def main() -> int:
    eng = QuantumEngine()
    print("=== FSOT-Quantum (fsot_lib owned stack) ===")
    print("implementation: FSOT-GPU fsot_lib")
    print(f"device: {eng.device}")
    print(f"Θ = {COLLAPSE_THRESHOLD}")
    print(f"S(QM) = {domain_scalar(DOMAIN_SPIN_LAW)}")
    print(f"S(QC) = {domain_scalar(DOMAIN_COMPUTE)}")

    reg = TritRegister.from_bits([0, 0], domain=DOMAIN_COMPUTE)
    print("bell init:", reg.spins)
    print("bell out: ", eng.run(reg, bell_analog()).spins)

    c = Circuit(3).h(0).h(1).cx(0, 1).cx(1, 2).measure()
    print("chain3:   ", eng.run(TritRegister.zeros(3), c).spins)

    print("pack:     ", [hex(w) for w in eng.pack([1, -1, 0, 1])])
    print("collapse: ", eng.collapse_field([1.0, -1.0, 0.0, COLLAPSE_THRESHOLD + 0.01]))

    smoke = eng.smoke()
    out = ROOT / "results" / "demo.json"
    out.write_text(json.dumps({"smoke_ok": smoke["ok"], "device": eng.device, "checks": {k: v.get("ok") for k, v in smoke["checks"].items()}}, indent=2), encoding="utf-8")
    print(f"smoke ok = {smoke['ok']} → {out}")
    return 0 if smoke["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
