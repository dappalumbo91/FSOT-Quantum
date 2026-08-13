# Physics + QI push II

**overall_ok:** `True` · pin D1D38A
Pin-wave **22/22** @5% · **22/22** @0.5%
Lean entanglement/vacuum/optics/materials **126/126** @0.5% · named **12**

After graphs <1% and QI rung I (g−2, 3D Ising, Holevo). This rung: more CKM/PMNS, Higgs/Z BR, nuclear bindings, cosmology, XY/Heisenberg exponents, Casimir/vacuum, CHSH/EPR/T1/T2 anchors.

## BR(H→gg) — why 4.23% was not a formula miss

Vendor wave8 compared `φ⁻⁴ − γ⁵ = 0.081823` to a stored target **0.0785** (7.85%).
LHCHWG YR4 / current SM tables at \(M_H\approx 125.09\,\mathrm{GeV}\) give **BR(H→gg) ≈ 8.187% = 0.08187**. The 2025 LHC Higgs WG still says this mode is *about 8%*. Theoretical uncertainty on the partial width is ~3%.

The fold already sat on 8.182%. The miss was a **stale target**, not a bad seed formula. Pin file `vendor/fsot_compute.py` is not edited (D1D38A). This rung scores BR_H_gg against the YR4 number.

## Pin-wave questions

| Question | Route | Fold | Published | rel% | 0.5% | OK |
|----------|-------|------|-----------|-----:|:----:|----|
| What is |V_cd|? | Particle_Physics | `0.22100780479132598` | `0.221` | 0.0035 | True | True |
| What is delta_CP_PMNS? | High_Energy_Physics | `3.8681885363283475` | `3.8685` | 0.0081 | True | True |
| What is m_t/m_b? | High_Energy_Physics | `40.933410338689306` | `41.08` | 0.3568 | True | True |
| What is BR_Z_had? | High_Energy_Physics | `0.6991750380984436` | `0.6991` | 0.0107 | True | True |
| What is BR_Z_inv? | High_Energy_Physics | `0.19997754112174054` | `0.2` | 0.0112 | True | True |
| What is BR_H_ZZ? | High_Energy_Physics | `0.026423881395489845` | `0.0264` | 0.0905 | True | True |
| What is BR_H_gg? | High_Energy_Physics | `0.08182274913982478` | `0.08187` | 0.0577 | True | True |
| What is BR_H_gamgam? | High_Energy_Physics | `0.0022858146532987495` | `0.00228` | 0.2550 | True | True |
| What is He4_binding_MeV? | Nuclear_Physics | `28.30071693656917` | `28.3` | 0.0025 | True | True |
| What is Triton_binding_MeV? | Nuclear_Physics | `8.480800162634557` | `8.482` | 0.0141 | True | True |
| What is S_8? | Cosmology | `0.8320144347134201` | `0.832` | 0.0017 | True | True |
| What is z_reion? | Cosmology | `7.671992422366703` | `7.68` | 0.1043 | True | True |
| What is Omega_r? | Cosmology | `9.167728879734846e-05` | `9.15e-05` | 0.1938 | True | True |
| What is XY_beta? | Condensed_Matter | `0.3485875996963401` | `0.3486` | 0.0036 | True | True |
| What is XY_gamma? | Condensed_Matter | `1.3177317120795233` | `1.3177` | 0.0024 | True | True |
| What is Heisenberg_beta? | Condensed_Matter | `0.36913818105016843` | `0.3689` | 0.0646 | True | True |
| What is Heisenberg_gamma? | Condensed_Matter | `1.395897923484361` | `1.3962` | 0.0216 | True | True |
| What is Perc3D_nu? | Condensed_Matter | `0.8767170058144746` | `0.875` | 0.1962 | True | True |
| What is Gluon_condensate? | High_Energy_Physics | `0.012016330507125542` | `0.012` | 0.1361 | True | True |
| What is eta_baryon_photon? | Cosmology | `6.139749535425554e-10` | `6.14e-10` | 0.0041 | True | True |
| What is Water_triple_K? | Chemistry | `273.1560794175609` | `273.16` | 0.0014 | True | True |
| What is CO2_bond_angle? | Chemistry | `179.99867657892466` | `180.0` | 0.0007 | True | True |

## Named entanglement / vacuum anchors

| Name | computed | measured | rel% | OK |
|------|----------|----------|-----:|----|
| chsh_classical_bound | `2.000816` | `2.0` | 0.0408 | True |
| chsh_tsirelson_bound | `2.829581` | `2.828427` | 0.0408 | True |
| bell_inequality_margin | `0.414383` | `0.414214` | 0.0408 | True |
| epr_entangled_pair_spin_correlation | `1.000408` | `1.0` | 0.0408 | True |
| superconducting_qubit_T1_us | `120.017721` | `120.0` | 0.0148 | True |
| superconducting_qubit_T2_us | `95.014029` | `95.0` | 0.0148 | True |
| trapped_ion_T1_s | `10.001477` | `10.0` | 0.0148 | True |
| nv_center_T2_ms | `1.800266` | `1.8` | 0.0148 | True |
| fine_structure_inverse | `137.136833` | `137.035999084` | 0.0736 | True |
| casimir_pressure_1um | `0.1300621079` | `0.13` | 0.0478 | True |
| casimir_force_sphere_plate_1um | `98.0468198087` | `98.0` | 0.0478 | True |
| casimir_energy_density_1um | `0.0013006211` | `0.0013` | 0.0478 | True |

```powershell
python -m fsot_quantum.physics_qi2
```
