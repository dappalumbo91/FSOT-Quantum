# Stale-target audit — vendor table vs current literature

**overall_ok:** `True` · pin D1D38A **not edited**
Cited rows **20/20** fold-vs-literature @0.5% · stale vendor fields **1**

Same method as `docs/BR_H_GG.md`. If the stored vendor target is old and the formula already matches YR4/PDG, that is not a formula miss.

Three earlier 0.5% misses were **wrong objects**, not broken seeds. Diagnosis: `docs/MISS_THREE.md`.

- `|V_cb|` is scored against PDG **inclusive** 0.0422. Exclusive 0.0398 is the \(V_{cb}\) puzzle — a different extraction, not a retune.
- \(H\to\gamma\gamma\) and \(H\to Z\gamma\) are scored at **MH = 125.00 GeV** (the table the pin formulas were written against). YR4 125.09 GeV centrals sit inside the recommended theory bands (~2.8% and ~6%).

## Stale vendor fields (vendor vs literature > 0.5%)

| Name | vendor | literature | vendor vs lit | fold | fold vs lit |
|------|--------|------------|--------------:|------|------------:|
| BR_H_gg | `0.0785` | `0.08187` (LHCHWG YR4 SM BR(H→gg) MH≈125.09 GeV) | 4.116% | `0.08182274913982478` | 0.0577% |

## All cited rows

| Name | fold vs lit | fold vs vendor | stale vendor? | 0.5% vs lit |
|------|------------:|---------------:|:-------------:|:-----------:|
| sin2_theta_W | 0.0009% | 0.0009% | False | True |
| 1/alpha_em | 0.0001% | 0.0001% | False | True |
| |V_us| | 0.0100% | 0.0100% | False | True |
| |V_cb| | 0.0019% | 0.0019% | False | True |
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
| BR_H_gamgam | 0.2550% | 0.2550% | False | True |
| BR_H_Zgam | 0.2708% | 0.2708% | False | True |
| He4_binding_MeV | 0.0179% | 0.0025% | False | True |
| |V_tb| | 0.0024% | 0.0024% | False | True |
| m_mu/m_e | 0.0007% | 0.0007% | False | True |
| (g-2)/2_electron | 0.0007% | 0.0009% | False | True |

## Higgs photon channels vs 125.09 GeV (theory band, not the 0.5% gate)

| Name | fold vs 125.00 | fold vs 125.09 | theory unc | inside theory? |
|------|---------------:|---------------:|-----------:|:--------------:|
| BR_H_gamgam | 0.2550% | 0.6967% | ~2.8% | True |
| BR_H_Zgam | 0.2708% | 0.9827% | ~6.0% | True |

Exclusive \(|V_{cb}|\) = 0.0398 is **not** in the cited pass/fail table. It is a different measurement. See `docs/MISS_THREE.md`.

```powershell
python -m fsot_quantum.stale_targets
```
