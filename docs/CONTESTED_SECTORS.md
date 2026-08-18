# Contested sectors — aligned with FSOT-2.1-Lean

**overall_ok:** `True` · **14/14** · pin D1D38A **not edited**

These are the open-science tensions Lean already monitors ([CONTESTED_SECTOR_WATCH](https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/predictions/reports/CONTESTED_SECTOR_WATCH.md)). Computed here from the same pin. Hubble tools use BH→WH bubble-bleed.

| Name | Formula | Fold | Published | rel% | gate | OK |
|------|---------|------|-----------|-----:|-----:|:--:|
| H0_Planck_CMB | `H0_global·(1 − bleed)` | `67.38395076840948` | `67.4` | 0.0238 | 0.5% | True |
| H0_SH0ES | `H0_global·(1 + 5.05·bleed)` | `73.7733924397876` | `73.04` | 1.0041 | 2.5% | True |
| H0_Carnegie | `H0_global·(1 + 2.04·bleed)` | `70.5945131950193` | `69.8` | 1.1383 | 2.5% | True |
| r_c_Fornax_kpc | `η_eff·φ − POOF` | `0.6020461466908882` | `0.6` | 0.3410 | 0.5% | True |
| Lithium_problem_factor | `π·C_eff` | `3.008710204079519` | `3.0` | 0.2903 | 0.5% | True |
| m_H_GeV | `(θ_S + e³)/C_factor⁷ / 1000` | `125.20001875723796` | `125.25` | 0.0399 | 0.5% | True |
| S_8 | `ψ_con/√γ` | `0.8320144347134201` | `0.832` | 0.0017 | 0.5% | True |
| N_eff | `P_new·e·π + ln(φ)` | `3.045713454288361` | `3.046` | 0.0094 | 0.5% | True |
| Omega_Lambda | `S_quant/e + γ²` | `0.6846890475252997` | `0.6847` | 0.0016 | 0.5% | True |
| sigma_8 | `|S_cosm|·S_quant + |Chaos|` | `0.8111240047382514` | `0.8111` | 0.0030 | 0.5% | True |
| tau_reion | `φ·|Chaos| − ln(φ)` | `0.05439655350230806` | `0.0544` | 0.0063 | 0.5% | True |
| D_H_ratio | `1/(π⁴·e⁶)` | `2.5446825859417006e-05` | `2.547e-05` | 0.0910 | 0.5% | True |
| w0 | `−P_new·π/G` | `-1.0299812921372637` | `-1.03` | 0.0018 | 0.5% | True |
| alpha_s(M_Z) | `1/(e·π)` | `0.11709966304863832` | `0.1179` | 0.6788 | 0.9% | True |

α_s(M_Z) keeps the vendor 0.9% band (PDG 1σ edge). SH0ES / Carnegie keep Lean’s 2.5% contested-sector band.

```powershell
python -m fsot_quantum.contested_sectors
```
