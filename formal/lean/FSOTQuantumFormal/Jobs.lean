/-
  Hired QC job facts (integer) — twin of Zig jobs + Python ask_qc.
  Same surface as Coq Jobs.v, Isabelle Jobs.thy, F* Jobs.fst.
-/

import FSOTQuantumFormal.Fold

namespace FSOT.Quantum.Jobs

-- Shor-role periods
theorem seven_pow_four_mod_fifteen : 7 ^ 4 % 15 = 1 := by native_decide
theorem two_pow_four_mod_fifteen : 2 ^ 4 % 15 = 1 := by native_decide
theorem five_pow_six_mod_twentyone : 5 ^ 6 % 21 = 1 := by native_decide
theorem two_pow_ten_mod_thirtythree : 2 ^ 10 % 33 = 1 := by native_decide
theorem eight_pow_eight_mod_fiftyone : 8 ^ 8 % 51 = 1 := by native_decide

-- Factor composites (Shor end-job)
theorem gcd_three_fifteen : Nat.gcd 3 15 = 3 := by native_decide
theorem gcd_five_fifteen : Nat.gcd 5 15 = 5 := by native_decide
theorem factor_fifteen : 3 * 5 = 15 := by native_decide
theorem factor_twentyone : 3 * 7 = 21 := by native_decide
theorem factor_thirtythree : 3 * 11 = 33 := by native_decide
theorem seven_sq_mod_fifteen : 7 ^ 2 % 15 = 4 := by native_decide
theorem shor_gcd_fold_fifteen :
    Nat.gcd (4 - 1) 15 = 3 ∧ Nat.gcd (4 + 1) 15 = 5 := by native_decide

-- CNOT bits (control=1 flips target)
theorem cnot_one_zero : 1 ^^^ 0 = 1 := by native_decide
theorem cnot_one_one : 1 ^^^ 1 = 0 := by native_decide

-- Fold vs Hilbert cost
theorem fold8 : Fold.foldBudget 8 = 195 := Fold.foldBudget_eight
theorem fold8_lt_hilbert : Fold.foldBudget 8 < Fold.hilbertAmps 8 := Fold.fold_lt_hilbert_eight

theorem jobs_surface :
    7 ^ 4 % 15 = 1
    ∧ 5 ^ 6 % 21 = 1
    ∧ 3 * 5 = 15
    ∧ Fold.foldBudget 8 < Fold.hilbertAmps 8
    ∧ Nat.gcd 3 15 = 3 := by
  refine ⟨seven_pow_four_mod_fifteen, five_pow_six_mod_twentyone, factor_fifteen,
    fold8_lt_hilbert, gcd_three_fifteen⟩

end FSOT.Quantum.Jobs
