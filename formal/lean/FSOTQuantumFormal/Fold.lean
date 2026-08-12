/-
  FSOT-Quantum — fold-vs-Hilbert cost contracts (Lean 4).
  Runtime twin: fsot_quantum/fold_complexity.py fold_budget_formal
-/

namespace FSOT.Quantum.Fold

/-- Hilbert amplitude count for n qubits. -/
def hilbertAmps (n : Nat) : Nat := 2 ^ n

/-- Integer fold budget proxy: 3 · n · 7 + 27 (mid depth · 10φ/(1+φ) bound · Metatron). -/
def foldBudget (n : Nat) : Nat := 3 * n * 7 + 27

theorem foldBudget_zero : foldBudget 0 = 27 := by native_decide
theorem foldBudget_one : foldBudget 1 = 48 := by native_decide
theorem hilbertAmps_eight : hilbertAmps 8 = 256 := by native_decide
theorem foldBudget_eight : foldBudget 8 = 195 := by native_decide

theorem fold_lt_hilbert_eight : foldBudget 8 < hilbertAmps 8 := by native_decide
theorem fold_lt_hilbert_sixteen : foldBudget 16 < hilbertAmps 16 := by native_decide
theorem fold_lt_hilbert_twenty : foldBudget 20 < hilbertAmps 20 := by native_decide
theorem fold_lt_hilbert_thirtytwo : foldBudget 32 < hilbertAmps 32 := by native_decide

/-- Alias used by surface stamp. -/
theorem fold_cost_surface :
    foldBudget 8 < hilbertAmps 8
    ∧ foldBudget 16 < hilbertAmps 16
    ∧ foldBudget 32 < hilbertAmps 32 := by
  refine ⟨fold_lt_hilbert_eight, fold_lt_hilbert_sixteen, fold_lt_hilbert_thirtytwo⟩

end FSOT.Quantum.Fold
