theory Pack
  imports Trinary
begin

definition bits_per_trit :: "nat" where
  "bits_per_trit = 2"

lemma pack_capacity: "states_per_u64 * bits_per_trit = 64"
  by (simp add: states_per_u64_def bits_per_trit_def)

lemma of_bits_three_none: "spin_of_bits 3 = None"
  by (simp add: spin_of_bits_def)

lemma to_bits_inj: "spin_to_bits a = spin_to_bits b ==> a = b"
  by (cases a; cases b) simp_all

end
