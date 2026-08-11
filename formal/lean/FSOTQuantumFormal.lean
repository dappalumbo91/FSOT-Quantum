/-
  FSOT-Quantum multiprover — Lean 4 master integrator.

  Authority: pin D1D38A (vendor/fsot_compute.py)
  Runtime twin: fsot_lib + fsot_quantum (Python)
  Sibling provers: Coq, Isabelle/HOL

  Spins: −1 down · 0 superposed · +1 up
  Pack codes: 0 / 1 / 2  (2 bits each, 32 per UInt64)
-/

import FSOTQuantumFormal.Trinary
import FSOTQuantumFormal.Gates
import FSOTQuantumFormal.Pack
import FSOTQuantumFormal.Domains

namespace FSOT.Quantum

/-- Stamp: multiprover quantum formal surface is closed for this edition. -/
theorem quantum_formal_surface_ok :
    statesPerU64 = 32
    ∧ Domain.QuantumMechanics.D_eff = 6
    ∧ Domain.QuantumComputing.D_eff = 11 := by
  exact ⟨statesPerU64_eq, Domain.QM_D_eff, Domain.QC_D_eff⟩

end FSOT.Quantum
