(* FSOT-Quantum — Coq trinary spins (parallel to Lean FSOTQuantumFormal.Trinary) *)
(* Pin D1D38A · codes 0=down 1=super 2=up · signed −1 0 +1 *)

From Stdlib Require Import ZArith.
From Stdlib Require Import Lia.

Inductive Spin : Type :=
  | SpinDown
  | Superposed
  | SpinUp.

Definition spin_to_bits (s : Spin) : nat :=
  match s with
  | SpinDown => 0
  | Superposed => 1
  | SpinUp => 2
  end.

Definition spin_of_bits (n : nat) : option Spin :=
  match n with
  | 0 => Some SpinDown
  | 1 => Some Superposed
  | 2 => Some SpinUp
  | _ => None
  end.

Lemma spin_roundtrip_bits : forall s, spin_of_bits (spin_to_bits s) = Some s.
Proof.
  intros s; destruct s; reflexivity.
Qed.

Definition spin_to_int (s : Spin) : Z :=
  match s with
  | SpinDown => (-1)%Z
  | Superposed => 0%Z
  | SpinUp => 1%Z
  end.

Definition states_per_u64 : nat := 32.

Lemma states_per_u64_eq : states_per_u64 = 32.
Proof. reflexivity. Qed.

Definition valid_code (n : nat) : Prop := n <= 2.

Lemma to_bits_valid : forall s, valid_code (spin_to_bits s).
Proof.
  intros s; destruct s; unfold valid_code; simpl; lia.
Qed.
