(* FSOT-Quantum — Coq pack contracts *)

Require Import Trinary.

Definition bits_per_trit : nat := 2.

Lemma pack_capacity : states_per_u64 * bits_per_trit = 64.
Proof. reflexivity. Qed.

Lemma of_bits_three_none : spin_of_bits 3 = None.
Proof. reflexivity. Qed.

Lemma to_bits_inj : forall a b, spin_to_bits a = spin_to_bits b -> a = b.
Proof.
  intros a b H; destruct a; destruct b; simpl in H; try reflexivity; discriminate.
Qed.
