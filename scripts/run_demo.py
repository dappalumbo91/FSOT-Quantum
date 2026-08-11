#!/usr/bin/env python3
"""Demo: FSOT trinary quantum pathway on host (GPU optional)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.circuit import Circuit, bell_analog_circuit, deutsch_analog, run_circuit
from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW
from fsot_quantum.device import backend_info, batch_collapse_field, pack_spins
from fsot_quantum.qubit import TritRegister
from fsot_quantum.scalar import domain_scalar
from fsot_quantum.seeds import COLLAPSE_THRESHOLD, PIN_EXPECTED, pin_matches
from fsot_quantum.trinary import SPIN_DOWN, SPIN_UP, SUPERPOSED


def main() -> int:
    print("=== FSOT-Quantum demo ===")
    print(f"pin match D1D38A: {pin_matches()} (expected {PIN_EXPECTED})")
    print(f"Θ = C_eff·P_var = {COLLAPSE_THRESHOLD}")
    print(f"S({DOMAIN_SPIN_LAW}) = {domain_scalar(DOMAIN_SPIN_LAW)}")
    print(f"S({DOMAIN_COMPUTE})  = {domain_scalar(DOMAIN_COMPUTE)}")
    print("backend:", json.dumps(backend_info(), indent=2))

    print("\n-- Spin doctrine --")
    print(f"  DOWN={int(SPIN_DOWN)}  SUPER={int(SUPERPOSED)}  UP={int(SPIN_UP)}")

    print("\n-- Bell-analog circuit --")
    reg = TritRegister.from_bits([0, 0], domain=DOMAIN_COMPUTE)
    print("  init:", reg.spins)
    out = run_circuit(reg, bell_analog_circuit())
    print("  out: ", out.spins)

    print("\n-- Deutsch-analog circuit --")
    reg2 = TritRegister.from_bits([0, 0], domain=DOMAIN_COMPUTE)
    out2 = run_circuit(reg2, deutsch_analog())
    print("  out: ", out2.spins)

    print("\n-- Manual superpose + CX chain (3 spins) --")
    c = Circuit(3).h(0).h(1).cx(0, 1).cx(1, 2).measure()
    reg3 = TritRegister.zeros(3, domain=DOMAIN_SPIN_LAW)
    out3 = run_circuit(reg3, c)
    print("  out: ", out3.spins)

    print("\n-- Pack / collapse host path --")
    words = pack_spins(out3.spins)
    print("  packed u64 words:", [hex(w) for w in words])
    field = [1.0, -1.0, 0.0, COLLAPSE_THRESHOLD + 0.01, -(COLLAPSE_THRESHOLD + 0.01)]
    print("  collapse:", batch_collapse_field(field))

    report = {
        "bell": out.spins,
        "deutsch": out2.spins,
        "chain3": out3.spins,
        "collapse_threshold": COLLAPSE_THRESHOLD,
        "S_QM": domain_scalar(DOMAIN_SPIN_LAW),
        "S_QC": domain_scalar(DOMAIN_COMPUTE),
        "pin_ok": pin_matches(),
    }
    outp = ROOT / "results" / "demo.json"
    outp.parent.mkdir(exist_ok=True)
    outp.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {outp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
