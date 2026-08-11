(* FSOT-Quantum — Hilbert dimension contracts (Coq) *)

From Stdlib Require Import Arith Lia.

Definition dim (n : nat) : nat := Nat.pow 2 n.

Lemma dim_zero : dim 0 = 1.
Proof. reflexivity. Qed.

Lemma dim_one : dim 1 = 2.
Proof. reflexivity. Qed.

Lemma dim_two : dim 2 = 4.
Proof. reflexivity. Qed.

Lemma dim_three : dim 3 = 8.
Proof. reflexivity. Qed.

Lemma dim_twelve : dim 12 = 4096.
Proof. reflexivity. Qed.
