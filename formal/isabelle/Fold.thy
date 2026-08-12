theory Fold
  imports Main
begin

definition hilbert_amps :: "nat => nat" where
  "hilbert_amps n = 2 ^ n"

definition fold_budget :: "nat => nat" where
  "fold_budget n = 3 * n * 7 + 27"

lemma fold_budget_zero: "fold_budget 0 = 27"
  by (simp add: fold_budget_def)

lemma fold_budget_one: "fold_budget 1 = 48"
  by (simp add: fold_budget_def)

lemma hilbert_amps_eight: "hilbert_amps 8 = 256"
  by (simp add: hilbert_amps_def)

lemma fold_budget_eight: "fold_budget 8 = 195"
  by (simp add: fold_budget_def)

lemma fold_lt_hilbert_eight: "fold_budget 8 < hilbert_amps 8"
  by (simp add: fold_budget_def hilbert_amps_def)

lemma fold_lt_hilbert_sixteen: "fold_budget 16 < hilbert_amps 16"
  by (simp add: fold_budget_def hilbert_amps_def)

lemma fold_lt_hilbert_thirtytwo: "fold_budget 32 < hilbert_amps 32"
  by (simp add: fold_budget_def hilbert_amps_def)

end
