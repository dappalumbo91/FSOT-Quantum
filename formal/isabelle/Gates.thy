theory Gates
  imports Trinary
begin

fun neg :: "spin => spin" where
  "neg SpinDown = SpinUp" |
  "neg Superposed = Superposed" |
  "neg SpinUp = SpinDown"

lemma neg_involutive: "neg (neg s) = s"
  by (cases s) simp_all

fun pair_spin :: "spin => spin => spin" where
  "pair_spin Superposed t = Superposed" |
  "pair_spin SpinDown Superposed = Superposed" |
  "pair_spin SpinUp Superposed = Superposed" |
  "pair_spin SpinUp SpinUp = SpinUp" |
  "pair_spin SpinDown SpinDown = SpinUp" |
  "pair_spin SpinUp SpinDown = SpinDown" |
  "pair_spin SpinDown SpinUp = SpinDown"

lemma pair_super_left: "pair_spin Superposed t = Superposed"
  by simp

definition consensus :: "spin => spin => spin" where
  "consensus a b = (if a = b then a else Superposed)"

lemma consensus_refl: "consensus s s = s"
  by (simp add: consensus_def)

fun cx_target :: "spin => spin => spin" where
  "cx_target Superposed t = Superposed" |
  "cx_target SpinUp t = neg t" |
  "cx_target SpinDown t = t"

lemma cx_control_up: "cx_target SpinUp t = neg t"
  by simp

lemma cx_control_down: "cx_target SpinDown t = t"
  by simp

lemma cx_control_super: "cx_target Superposed t = Superposed"
  by simp

end
