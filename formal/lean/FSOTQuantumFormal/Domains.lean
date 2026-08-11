/-
  FSOT-Quantum domain interfaces (Lean 4).

  Runtime: fsot_quantum/domains.py + vendor/fsot_compute.py DOMAINS
  Pin D1D38A — preregistered folds, not free parameters.
-/

namespace FSOT.Quantum.Domain

structure DomainConfig where
  name : String
  D_eff : Nat
  hits : Nat
  observed : Bool
  deriving Repr

def QuantumMechanics : DomainConfig :=
  { name := "Quantum_Mechanics"
    D_eff := 6
    hits := 0
    observed := true }

def QuantumComputing : DomainConfig :=
  { name := "Quantum_Computing"
    D_eff := 11
    hits := 0
    observed := false }

theorem QM_D_eff : QuantumMechanics.D_eff = 6 := rfl
theorem QC_D_eff : QuantumComputing.D_eff = 11 := rfl
theorem QM_observed : QuantumMechanics.observed = true := rfl
theorem QC_unobserved : QuantumComputing.observed = false := rfl

/-- Compactification ceiling (FSOT fluid). -/
def compactificationCeiling : Nat := 25

theorem ceiling_eq : compactificationCeiling = 25 := rfl

/-- Both quantum domains sit strictly below the ceiling. -/
theorem QM_below_ceiling : QuantumMechanics.D_eff < compactificationCeiling := by
  native_decide

theorem QC_below_ceiling : QuantumComputing.D_eff < compactificationCeiling := by
  native_decide

end FSOT.Quantum.Domain

-- Re-export names used by FSOTQuantumFormal.lean
namespace FSOT.Quantum
export Domain (QuantumMechanics QuantumComputing)
end FSOT.Quantum
