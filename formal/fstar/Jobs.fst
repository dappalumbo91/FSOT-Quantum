module Jobs

/// Hired QC job facts — F* twin of Lean/Coq/Isabelle Jobs.
/// Integer only. Pin D1D38A.
/// F* 2026: no FStar.Mul; * and % are prelude.

let fold_budget (n: nat) : nat = 3 * n * 7 + 27
let hilbert_amps_eight : nat = 256

val fold_budget_eight: unit -> Lemma (fold_budget 8 == 195)
let fold_budget_eight () = ()

val fold8_lt_hilbert: unit -> Lemma (fold_budget 8 < hilbert_amps_eight)
let fold8_lt_hilbert () = ()

/// Shor-role: 7^4 ≡ 1 (mod 15)
let seven_to_the_four : nat = 7 * 7 * 7 * 7
val seven_pow_four_mod_fifteen: unit -> Lemma (seven_to_the_four % 15 == 1)
let seven_pow_four_mod_fifteen () = ()

/// 2^4 ≡ 1 (mod 15)
let two_to_the_four : nat = 2 * 2 * 2 * 2
val two_pow_four_mod_fifteen: unit -> Lemma (two_to_the_four % 15 == 1)
let two_pow_four_mod_fifteen () = ()

/// 5^6 ≡ 1 (mod 21)
let five_to_the_six : nat = 5 * 5 * 5 * 5 * 5 * 5
val five_pow_six_mod_twentyone: unit -> Lemma (five_to_the_six % 21 == 1)
let five_pow_six_mod_twentyone () = ()

/// 2^10 ≡ 1 (mod 33)
let two_to_the_ten : nat = 1024
val two_pow_ten_mod_thirtythree: unit -> Lemma (two_to_the_ten % 33 == 1)
let two_pow_ten_mod_thirtythree () = ()

/// Factor 15 / 21 / 33
val factor_fifteen: unit -> Lemma (3 * 5 == 15)
let factor_fifteen () = ()

val factor_twentyone: unit -> Lemma (3 * 7 == 21)
let factor_twentyone () = ()

val factor_thirtythree: unit -> Lemma (3 * 11 == 33)
let factor_thirtythree () = ()

/// Shor gcd fold on 15: 7^2 ≡ 4, 3|15, 5|15
val seven_sq_mod_fifteen: unit -> Lemma ((7 * 7) % 15 == 4)
let seven_sq_mod_fifteen () = ()

val shor_gcd_fold_fifteen: unit -> Lemma (
  15 % 3 == 0 /\ 15 % 5 == 0 /\ (4 - 1 == 3) /\ (4 + 1 == 5)
)
let shor_gcd_fold_fifteen () = ()

/// CNOT bits
let cnot_bit (c t: nat) : nat = (t + (c % 2)) % 2
val cnot_10: unit -> Lemma (cnot_bit 1 0 == 1)
let cnot_10 () = ()
val cnot_11: unit -> Lemma (cnot_bit 1 1 == 0)
let cnot_11 () = ()

val jobs_surface: unit -> Lemma (
  seven_to_the_four % 15 == 1 /\
  five_to_the_six % 21 == 1 /\
  3 * 5 == 15 /\
  fold_budget 8 < hilbert_amps_eight
)
let jobs_surface () = ()
