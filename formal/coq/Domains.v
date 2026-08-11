(* FSOT-Quantum — Coq domain interfaces *)

From Stdlib Require Import String.
From Stdlib Require Import Lia.
From Stdlib Require Import Arith.

Record DomainConfig : Type := mkDomain {
  d_name : string;
  d_eff : nat;
  d_hits : nat;
  d_observed : bool
}.

Definition Quantum_Mechanics : DomainConfig :=
  {| d_name := "Quantum_Mechanics"; d_eff := 6; d_hits := 0; d_observed := true |}.

Definition Quantum_Computing : DomainConfig :=
  {| d_name := "Quantum_Computing"; d_eff := 11; d_hits := 0; d_observed := false |}.

Lemma QM_D_eff : d_eff Quantum_Mechanics = 6.
Proof. reflexivity. Qed.

Lemma QC_D_eff : d_eff Quantum_Computing = 11.
Proof. reflexivity. Qed.

Lemma QM_observed : d_observed Quantum_Mechanics = true.
Proof. reflexivity. Qed.

Lemma QC_unobserved : d_observed Quantum_Computing = false.
Proof. reflexivity. Qed.

Definition compactification_ceiling : nat := 25.

Lemma QM_below_ceiling : d_eff Quantum_Mechanics < compactification_ceiling.
Proof.
  change (6 < 25).
  repeat constructor.
Qed.

Lemma QC_below_ceiling : d_eff Quantum_Computing < compactification_ceiling.
Proof.
  change (11 < 25).
  repeat constructor.
Qed.
