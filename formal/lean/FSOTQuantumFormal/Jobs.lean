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

-- Living Shor / QAOA integers (not tiny-N demos).
-- Far RSA-shaped pair from heights: similar bits, not twins.
theorem factor_far_rsa_shaped : 10007 * 1000003 = 10007030021 := by native_decide
theorem far_not_twin : 1000003 ≠ 10007 + 2 := by native_decide
-- log-N leftover: p−1 = 2·3·7·2381 sits in stage-2 (B, B2].
theorem pminus1_stage2_smooth : 100003 - 1 = 2 * 3 * 7 * 2381 := by native_decide
-- B = bitlen · ⌊eπ⌋ · ⌊π⌋. Seed floors 8 and 3. RSA-2048 B stays 49152.
theorem b_lock_unit : 8 * 3 = 24 := by native_decide
theorem b_lock_103 : 103 * 24 = 2472 := by native_decide
theorem b_lock_2048 : 2048 * 24 = 49152 := by native_decide
-- Gset aspiration <1% as an integer inequality (champions unmatched).
theorem g17_under_one_pct : 100 * (3047 - 3034) < 3047 := by native_decide
theorem g22_under_one_pct : 100 * (13359 - 13261) < 13359 := by native_decide

theorem living_jobs_surface :
    10007 * 1000003 = 10007030021
    ∧ 100003 - 1 = 2 * 3 * 7 * 2381
    ∧ 8 * 3 = 24
    ∧ 2048 * 24 = 49152
    ∧ 100 * (3047 - 3034) < 3047
    ∧ 100 * (13359 - 13261) < 13359 := by
  refine ⟨factor_far_rsa_shaped, pminus1_stage2_smooth, b_lock_unit,
    b_lock_2048, g17_under_one_pct, g22_under_one_pct⟩

end FSOT.Quantum.Jobs
