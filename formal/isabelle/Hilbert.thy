theory Hilbert
  imports Main
begin

definition dim :: "nat => nat" where
  "dim n = 2 ^ n"

lemma dim_zero: "dim 0 = 1"
  by (simp add: dim_def)

lemma dim_one: "dim 1 = 2"
  by (simp add: dim_def)

lemma dim_two: "dim 2 = 4"
  by (simp add: dim_def)

lemma dim_three: "dim 3 = 8"
  by (simp add: dim_def)

lemma dim_twelve: "dim 12 = 4096"
  by (simp add: dim_def)

end
