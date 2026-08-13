# Stale-target audit — vendor table vs current literature

**overall_ok:** `False` · pin D1D38A **not edited**
Cited rows **17/20** fold-vs-literature @0.5% · stale vendor fields **3**

Same method as `docs/BR_H_GG.md`. If the stored vendor target is old and the formula already matches YR4/PDG, that is not a formula miss.

## Stale vendor fields (vendor vs literature > 0.5%)

| Name | vendor | literature | vendor vs lit | fold | fold vs lit |
|------|--------|------------|--------------:|------|------------:|
| |V_cb| | `0.0422` | `0.0411` (PDG CKM |V_cb| (exclusive/inclusive average ~0.041)) | 2.676% | `0.04220081332791359` | 2.6784% |
| BR_H_gg | `0.0785` | `0.08187` (LHCHWG YR4 SM BR(H→gg) MH≈125.09 GeV) | 4.116% | `0.08182274913982478` | 0.0577% |
| BR_H_Zgam | `0.00153` | `0.001541` (LHCHWG YR4 SM BR(H→Zγ) MH≈125.09 GeV) | 0.714% | `0.0015258567671942072` | 0.9827% |

## All cited rows

| Name | fold vs lit | fold vs vendor | stale vendor? | 0.5% vs lit |
|------|------------:|---------------:|:-------------:|:-----------:|
| sin2_theta_W | 0.0009% | 0.0009% | False | True |
| 1/alpha_em | 0.0001% | 0.0001% | False | True |
| |V_us| | 0.0100% | 0.0100% | False | True |
| |V_cb| | 2.6784% | 0.0019% | True | False |
| Deuteron_binding_MeV | 0.0001% | 0.0001% | False | True |
| |V_ub| | 0.0089% | 0.0089% | False | True |
| BR_H_bb | 0.0042% | 0.0042% | False | True |
| BR_H_WW | 0.0021% | 0.0021% | False | True |
| |V_ud| | 0.0024% | 0.0007% | False | True |
| |V_cd| | 0.0035% | 0.0035% | False | True |
| |V_cs| | 0.0089% | 0.1452% | False | True |
| BR_H_ZZ | 0.0232% | 0.0905% | False | True |
| BR_H_gg | 0.0577% | 4.2328% | True | True |
| BR_H_cc | 0.0535% | 0.0881% | False | True |
| BR_H_gamgam | 0.6967% | 0.2550% | False | False |
| BR_H_Zgam | 0.9827% | 0.2708% | True | False |
| He4_binding_MeV | 0.0179% | 0.0025% | False | True |
| |V_tb| | 0.0024% | 0.0024% | False | True |
| m_mu/m_e | 0.0007% | 0.0007% | False | True |
| (g-2)/2_electron | 0.0007% | 0.0009% | False | True |

```powershell
python -m fsot_quantum.stale_targets
```
