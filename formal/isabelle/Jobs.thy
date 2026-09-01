theory Jobs
  imports Fold
begin

(* Shor-role periods *)
lemma seven_pow_four_mod_fifteen: "(7::nat) ^ 4 mod 15 = 1"
  by simp

lemma two_pow_four_mod_fifteen: "(2::nat) ^ 4 mod 15 = 1"
  by simp

lemma five_pow_six_mod_twentyone: "(5::nat) ^ 6 mod 21 = 1"
  by simp

lemma two_pow_ten_mod_thirtythree: "(2::nat) ^ 10 mod 33 = 1"
  by simp

lemma eight_pow_eight_mod_fiftyone: "(8::nat) ^ 8 mod 51 = 1"
  by simp

(* Factor composites (Shor end-job) *)
lemma gcd_three_fifteen: "gcd (3::nat) 15 = 3"
  by simp

lemma gcd_five_fifteen: "gcd (5::nat) 15 = 5"
  by simp

lemma factor_fifteen: "(3::nat) * 5 = 15"
  by simp

lemma factor_twentyone: "(3::nat) * 7 = 21"
  by simp

lemma factor_thirtythree: "(3::nat) * 11 = 33"
  by simp

lemma seven_sq_mod_fifteen: "(7::nat) ^ 2 mod 15 = 4"
  by simp

lemma shor_gcd_fold_fifteen:
  "gcd ((4::nat) - 1) 15 = 3 \<and> gcd ((4::nat) + 1) 15 = 5"
  by simp

(* Fold vs Hilbert cost *)
lemma fold8_job: "fold_budget 8 = 195"
  by (rule fold_budget_eight)

lemma fold8_lt_job: "fold_budget 8 < hilbert_amps 8"
  by (rule fold_lt_hilbert_eight)

lemma jobs_surface:
  "(7::nat) ^ 4 mod 15 = 1
   \<and> (5::nat) ^ 6 mod 21 = 1
   \<and> (3::nat) * 5 = 15
   \<and> fold_budget 8 < hilbert_amps 8
   \<and> gcd (3::nat) 15 = 3"
  by (simp add: fold8_lt_job)

(* Living Shor / QAOA integers (not tiny-N demos). *)
lemma factor_far_rsa_shaped: "(10007::nat) * 1000003 = 10007030021"
  by simp

lemma far_not_twin: "(1000003::nat) \<noteq> 10007 + 2"
  by simp

lemma pminus1_stage2_smooth: "(100003::nat) - 1 = 2 * 3 * 7 * 2381"
  by simp

lemma b_lock_unit: "(8::nat) * 3 = 24"
  by simp

lemma b_lock_103: "(103::nat) * 24 = 2472"
  by simp

lemma b_lock_2048: "(2048::nat) * 24 = 49152"
  by simp

lemma g17_under_one_pct: "100 * ((3047::nat) - 3034) < 3047"
  by simp

lemma g22_under_one_pct: "100 * ((13359::nat) - 13261) < 13359"
  by simp

lemma living_jobs_surface:
  "(10007::nat) * 1000003 = 10007030021
   \<and> (100003::nat) - 1 = 2 * 3 * 7 * 2381
   \<and> (8::nat) * 3 = 24
   \<and> (2048::nat) * 24 = 49152
   \<and> 100 * ((3047::nat) - 3034) < 3047
   \<and> 100 * ((13359::nat) - 13261) < 13359"
  by simp

end
