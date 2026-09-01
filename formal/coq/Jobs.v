(* Hired QC job facts — Coq twin of Lean/Isabelle/F* Jobs. Pin D1D38A. *)
From Stdlib Require Import Arith Lia NArith.
Require Import Fold.

(* Shor-role periods *)
Lemma seven_pow_four_mod_fifteen : Nat.pow 7 4 mod 15 = 1.
Proof. reflexivity. Qed.

Lemma two_pow_four_mod_fifteen : Nat.pow 2 4 mod 15 = 1.
Proof. reflexivity. Qed.

Lemma five_pow_six_mod_twentyone : Nat.pow 5 6 mod 21 = 1.
Proof. reflexivity. Qed.

Lemma two_pow_ten_mod_thirtythree : Nat.pow 2 10 mod 33 = 1.
Proof. reflexivity. Qed.

Lemma eight_pow_eight_mod_fiftyone : Nat.pow 8 8 mod 51 = 1.
Proof. reflexivity. Qed.

(* Factor composites (Shor end-job) *)
Lemma gcd_three_fifteen : Nat.gcd 3 15 = 3.
Proof. reflexivity. Qed.

Lemma gcd_five_fifteen : Nat.gcd 5 15 = 5.
Proof. reflexivity. Qed.

Lemma factor_fifteen : 3 * 5 = 15.
Proof. reflexivity. Qed.

Lemma factor_twentyone : 3 * 7 = 21.
Proof. reflexivity. Qed.

Lemma factor_thirtythree : 3 * 11 = 33.
Proof. reflexivity. Qed.

Lemma seven_sq_mod_fifteen : Nat.pow 7 2 mod 15 = 4.
Proof. reflexivity. Qed.

Lemma shor_gcd_fold_fifteen :
  Nat.gcd (4 - 1) 15 = 3 /\ Nat.gcd (4 + 1) 15 = 5.
Proof. split; reflexivity. Qed.

(* Fold vs Hilbert cost *)
Lemma fold8_job : fold_budget 8 = 195.
Proof. apply fold_budget_eight. Qed.

Lemma fold8_lt_job : fold_budget 8 < hilbert_amps 8.
Proof. apply fold_lt_hilbert_eight. Qed.

Lemma jobs_surface :
  Nat.pow 7 4 mod 15 = 1
  /\ Nat.pow 5 6 mod 21 = 1
  /\ 3 * 5 = 15
  /\ fold_budget 8 < hilbert_amps 8
  /\ Nat.gcd 3 15 = 3.
Proof.
  split; [exact seven_pow_four_mod_fifteen|].
  split; [exact five_pow_six_mod_twentyone|].
  split; [exact factor_fifteen|].
  split; [exact fold8_lt_job|].
  exact gcd_three_fifteen.
Qed.

(* Living Shor / QAOA integers (not tiny-N demos).
   Large products use binary N — unary nat OOMs Coq. *)
Lemma factor_far_rsa_shaped : (10007 * 1000003 = 10007030021)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma far_not_twin : (1000003 <> 10007 + 2)%N.
Proof. vm_compute. discriminate. Qed.

Lemma pminus1_stage2_smooth : (100003 - 1 = 2 * 3 * 7 * 2381)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma b_lock_unit : (8 * 3 = 24)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma b_lock_103 : (103 * 24 = 2472)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma b_lock_2048 : (2048 * 24 = 49152)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma g17_under_one_pct : (100 * (3047 - 3034) <? 3047 = true)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma g22_under_one_pct : (100 * (13359 - 13261) <? 13359 = true)%N.
Proof. vm_compute. reflexivity. Qed.

Lemma living_jobs_surface :
  (10007 * 1000003 = 10007030021)%N
  /\ (100003 - 1 = 2 * 3 * 7 * 2381)%N
  /\ (8 * 3 = 24)%N
  /\ (2048 * 24 = 49152)%N
  /\ (100 * (3047 - 3034) <? 3047 = true)%N
  /\ (100 * (13359 - 13261) <? 13359 = true)%N.
Proof.
  split; [exact factor_far_rsa_shaped|].
  split; [exact pminus1_stage2_smooth|].
  split; [exact b_lock_unit|].
  split; [exact b_lock_2048|].
  split; [exact g17_under_one_pct|].
  exact g22_under_one_pct.
Qed.
