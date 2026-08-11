theory Domains
  imports Main
begin

datatype domain_config = DomainConfig string nat nat bool

fun d_name :: "domain_config => string" where
  "d_name (DomainConfig n e h obs) = n"

fun d_eff :: "domain_config => nat" where
  "d_eff (DomainConfig n e h obs) = e"

fun d_hits :: "domain_config => nat" where
  "d_hits (DomainConfig n e h obs) = h"

fun d_observed :: "domain_config => bool" where
  "d_observed (DomainConfig n e h obs) = obs"

definition Quantum_Mechanics :: "domain_config" where
  "Quantum_Mechanics = DomainConfig ''Quantum_Mechanics'' 6 0 True"

definition Quantum_Computing :: "domain_config" where
  "Quantum_Computing = DomainConfig ''Quantum_Computing'' 11 0 False"

lemma QM_D_eff: "d_eff Quantum_Mechanics = 6"
  by (simp add: Quantum_Mechanics_def)

lemma QC_D_eff: "d_eff Quantum_Computing = 11"
  by (simp add: Quantum_Computing_def)

lemma QM_observed: "d_observed Quantum_Mechanics = True"
  by (simp add: Quantum_Mechanics_def)

lemma QC_unobserved: "d_observed Quantum_Computing = False"
  by (simp add: Quantum_Computing_def)

definition compactification_ceiling :: "nat" where
  "compactification_ceiling = 25"

lemma QM_below_ceiling: "d_eff Quantum_Mechanics < compactification_ceiling"
  by (simp add: Quantum_Mechanics_def compactification_ceiling_def)

lemma QC_below_ceiling: "d_eff Quantum_Computing < compactification_ceiling"
  by (simp add: Quantum_Computing_def compactification_ceiling_def)

end
