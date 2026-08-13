(* FSOT-Quantum — fold-vs-Hilbert cost contracts (Coq) *)

From Stdlib Require Import Arith Lia.

Definition hilbert_amps (n : nat) : nat := Nat.pow 2 n.
Definition fold_budget (n : nat) : nat := 3 * n * 7 + 27.

Lemma fold_budget_zero : fold_budget 0 = 27.
Proof. reflexivity. Qed.

Lemma fold_budget_one : fold_budget 1 = 48.
Proof. reflexivity. Qed.

Lemma hilbert_amps_eight : hilbert_amps 8 = 256.
Proof. reflexivity. Qed.

Lemma fold_budget_eight : fold_budget 8 = 195.
Proof. reflexivity. Qed.

Lemma fold_lt_hilbert_eight : fold_budget 8 < hilbert_amps 8.
Proof. unfold fold_budget, hilbert_amps. simpl. lia. Qed.

Lemma fold_lt_hilbert_sixteen : fold_budget 16 < hilbert_amps 16.
Proof. unfold fold_budget, hilbert_amps. simpl. lia. Qed.

Lemma fold_lt_hilbert_thirtytwo : fold_budget 32 < hilbert_amps 32.
Proof.
  unfold fold_budget. simpl.
  unfold hilbert_amps.
  apply Nat.lt_trans with (m := Nat.pow 2 10).
  - simpl. lia.
  - apply Nat.pow_lt_mono_r; lia.
Qed.

(* Universal scale K ≈ 0.420222 — integer micro twin. S = K(T1+T2+T3). *)
Definition k_micro : nat := 420222.
Definition fold_work_k (n : nat) : nat := (n * 1000000 + 420221) / k_micro + 27.

Lemma fold_work_k_eight : fold_work_k 8 = 47.
Proof. vm_compute. reflexivity. Qed.

Lemma fold_work_k_sixtyfour : fold_work_k 64 = 180.
Proof. vm_compute. reflexivity. Qed.

Lemma fold_work_k_eight_lt : fold_work_k 8 < hilbert_amps 8.
Proof. vm_compute. apply Nat.ltb_lt. reflexivity. Qed.
