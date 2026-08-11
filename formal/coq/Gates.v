(* FSOT-Quantum — Coq gate algebra (parallel to Lean Gates.lean) *)

Require Import Trinary.

Definition neg (s : Spin) : Spin :=
  match s with
  | SpinDown => SpinUp
  | Superposed => Superposed
  | SpinUp => SpinDown
  end.

Lemma neg_involutive : forall s, neg (neg s) = s.
Proof.
  intros s; destruct s; reflexivity.
Qed.

Definition pair_spin (a b : Spin) : Spin :=
  match a, b with
  | Superposed, _ => Superposed
  | _, Superposed => Superposed
  | SpinUp, SpinUp => SpinUp
  | SpinDown, SpinDown => SpinUp
  | SpinUp, SpinDown => SpinDown
  | SpinDown, SpinUp => SpinDown
  end.

Lemma pair_super_left : forall t, pair_spin Superposed t = Superposed.
Proof.
  intros t; destruct t; reflexivity.
Qed.

Definition Spin_eq_dec : forall a b : Spin, {a = b} + {a <> b}.
Proof.
  decide equality.
Defined.

Definition consensus (a b : Spin) : Spin :=
  match Spin_eq_dec a b with
  | left _ => a
  | right _ => Superposed
  end.

Lemma consensus_refl : forall s, consensus s s = s.
Proof.
  intros s; unfold consensus; destruct (Spin_eq_dec s s) as [E|N].
  - reflexivity.
  - exfalso; apply N; reflexivity.
Qed.

Definition cx_target (c t : Spin) : Spin :=
  match c with
  | Superposed => Superposed
  | SpinUp => neg t
  | SpinDown => t
  end.

Lemma cx_control_up : forall t, cx_target SpinUp t = neg t.
Proof. reflexivity. Qed.

Lemma cx_control_down : forall t, cx_target SpinDown t = t.
Proof. reflexivity. Qed.

Lemma cx_control_super : forall t, cx_target Superposed t = Superposed.
Proof. reflexivity. Qed.
