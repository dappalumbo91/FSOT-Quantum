/-
  FSOT-Quantum multiprover — Lean 4 master integrator.

  Authority: pin D1D38A (vendor/fsot_compute.py)
  Runtime twin: fsot_lib + fsot_quantum (Python)
  Sibling provers: Coq, Isabelle/HOL, F*

  Spins: −1 down · 0 superposed · +1 up
  Pack codes: 0 / 1 / 2  (2 bits each, 32 per UInt64)
-/

import FSOTQuantumFormal.Trinary
import FSOTQuantumFormal.Gates
import FSOTQuantumFormal.Pack
import FSOTQuantumFormal.Domains
import FSOTQuantumFormal.Hilbert
import FSOTQuantumFormal.Fold
import FSOTQuantumFormal.Jobs

namespace FSOT.Quantum

/-- Stamp: multiprover quantum formal surface is closed for this edition. -/
theorem quantum_formal_surface_ok :
    statesPerU64 = 32
    ∧ Domain.QuantumMechanics.D_eff = 6
    ∧ Domain.QuantumComputing.D_eff = 11
    ∧ Hilbert.dim 12 = 4096
    ∧ Fold.foldBudget 8 < Fold.hilbertAmps 8
    ∧ 7 ^ 4 % 15 = 1 := by
  refine ⟨statesPerU64_eq, Domain.QM_D_eff, Domain.QC_D_eff, Hilbert.dim_twelve, Fold.fold_lt_hilbert_eight, ?_⟩
  exact Jobs.seven_pow_four_mod_fifteen

end FSOT.Quantum
