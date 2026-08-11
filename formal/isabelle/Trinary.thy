theory Trinary
  imports Main
begin

datatype spin = SpinDown | Superposed | SpinUp

fun spin_to_bits :: "spin => nat" where
  "spin_to_bits SpinDown = 0" |
  "spin_to_bits Superposed = 1" |
  "spin_to_bits SpinUp = 2"

definition spin_of_bits :: "nat => spin option" where
  "spin_of_bits n =
    (if n = 0 then Some SpinDown
     else if n = 1 then Some Superposed
     else if n = 2 then Some SpinUp
     else None)"

lemma spin_roundtrip_bits: "spin_of_bits (spin_to_bits s) = Some s"
  by (cases s) (simp_all add: spin_of_bits_def)

fun spin_to_int :: "spin => int" where
  "spin_to_int SpinDown = -1" |
  "spin_to_int Superposed = 0" |
  "spin_to_int SpinUp = 1"

definition states_per_u64 :: "nat" where
  "states_per_u64 = 32"

lemma states_per_u64_eq: "states_per_u64 = 32"
  by (simp add: states_per_u64_def)

definition valid_code :: "nat => bool" where
  "valid_code n = (n <= 2)"

lemma to_bits_valid: "valid_code (spin_to_bits s)"
  by (cases s) (simp_all add: valid_code_def)

end
