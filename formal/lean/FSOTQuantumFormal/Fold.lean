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

/-- Integer micro-K (round 0.420221664… · 10⁶). Universal scale in S = K(T1+T2+T3). -/
def kMicro : Nat := 420222

/-- K-scaled work: ceil(n / K) + 27  ≈  (n·10⁶ + 420221) / 420222 + 27 -/
def foldWorkK (n : Nat) : Nat := (n * 1000000 + 420221) / kMicro + 27

theorem foldWorkK_eight : foldWorkK 8 = 47 := by native_decide
theorem foldWorkK_sixtyfour : foldWorkK 64 = 180 := by native_decide
theorem foldWorkK_eight_lt_hilbert : foldWorkK 8 < hilbertAmps 8 := by native_decide
theorem foldWorkK_sixtyfour_lt_hilbert20 : foldWorkK 64 < 2 ^ 20 := by native_decide

end FSOT.Quantum.Fold
