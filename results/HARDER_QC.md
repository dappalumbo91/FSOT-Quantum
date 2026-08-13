# Harder questions — why they fund quantum computers

**overall_ok:** `True` · pin D1D38A · waves **20/20** @5% · **20/20** @0.5%
Gset official **3/3** (signed G11 skipped) · factors **6/6**

These are the numbers and jobs people wanted a QPU or a supercomputer for: CKM/PMNS mixing, 2D Ising criticality, nuclear bindings, Higgs/top ratios, hard MaxCut, factorization. Answered as domain folds.

## Particle / nuclear / Ising / EW

| Question | Route | Fold | Published | rel% | 0.5% | OK |
|----------|-------|------|-----------|-----:|:----:|----|
| What is |V_us|? | Particle_Physics | `0.22427764916395915` | `0.2243` | 0.0100 | True | True |
| What is |V_cb|? | Particle_Physics | `0.04220081332791359` | `0.0422` | 0.0019 | True | True |
| What is |V_ub|? | Particle_Physics | `0.0038196601125010513` | `0.00382` | 0.0089 | True | True |
| What is sin_theta_C? | Particle_Physics | `0.22759115424752144` | `0.22759` | 0.0005 | True | True |
| What is sin2_theta12? | High_Energy_Physics | `0.3069644297889016` | `0.307` | 0.0116 | True | True |
| What is sin2_theta23? | High_Energy_Physics | `0.5457666109860249` | `0.546` | 0.0427 | True | True |
| What is sin2_theta13? | High_Energy_Physics | `0.02201515822114412` | `0.022` | 0.0689 | True | True |
| What is Ising2D_beta? | Condensed_Matter | `0.3265324013682464` | `0.32653` | 0.0007 | True | True |
| What is Ising2D_nu? | Condensed_Matter | `0.6299845062655096` | `0.63002` | 0.0056 | True | True |
| What is Ising2D_gamma? | Condensed_Matter | `1.2371916616832948` | `1.2372` | 0.0007 | True | True |
| What is Deuteron_binding_MeV? | Nuclear_Physics | `2.224564648462528` | `2.224566` | 0.0001 | True | True |
| What is Neutron_lifetime_s? | Nuclear_Physics | `878.5928513922833` | `878.4` | 0.0220 | True | True |
| What is m_t/m_W? | High_Energy_Physics | `2.15000345864463` | `2.1498` | 0.0095 | True | True |
| What is m_H/m_W? | High_Energy_Physics | `1.5595014764878583` | `1.5595` | 0.0001 | True | True |
| What is m_n-m_p_MeV? | Nuclear_Physics | `1.2933328005542002` | `1.29333` | 0.0002 | True | True |
| What is Age_Gyr? | Cosmology | `13.787196119245323` | `13.787` | 0.0014 | True | True |
| What is Jarlskog_J? | Particle_Physics | `3.072771786665467e-05` | `3.08e-05` | 0.2347 | True | True |
| What is Gamma_Z/M_Z? | High_Energy_Physics | `0.027489782887668835` | `0.02749` | 0.0008 | True | True |
| What is BR_H_bb? | High_Energy_Physics | `0.5808757487636912` | `0.5809` | 0.0042 | True | True |
| What is m_H/m_t? | High_Energy_Physics | `0.7257068201623708` | `0.7256` | 0.0147 | True | True |

## Official MaxCut (Gset)

| Graph | n / cut | published | rel% | OK |
|-------|---------|-----------|-----:|----|
| G1.txt | n=`800` cut=`11538` | `11624` | 0.7398485891259463 | True |
| G14.txt | n=`800` cut=`3023` | `3064` | 1.3381201044386422 | True |
| G22.txt | n=`2000` cut=`13124` | `13359` | 1.7591137061157274 | True |

## Factors

| N | Factors | OK |
|---|---------|----|
| 10403 | `[101, 103]` | True |
| 8051 | `[83, 97]` | True |
| 1147 | `[31, 37]` | True |
| 6557 | `[79, 83]` | True |
| 8633 | `[89, 97]` | True |
| 1517 | `[37, 41]` | True |

## Lean quantum fabric ingested

- Quantum_Computing: n=`177` median%=`0.0002953462072651492` D_eff=`11`
- Quantum_Mechanics: n=`50` median%=`9.52387420324368e-05` D_eff=`6`
- Quantum_Optics: n=`50` median%=`9.52387420324368e-05` D_eff=`6`
- Quantum_Information: n=`21` median%=`0.0` D_eff=`11`
- Quantum_Mechanics_Entanglement_Depth_Panel: n=`21` median%=`0.014767` D_eff=`16`
- Quantum_Computing_Math_Depth_Panel: n=`77` median%=`0.014767` D_eff=`19`
- quantum_materials_benchmark.json: n=`168` median%=`0.01692529386942307` D_eff=`16`
- Founding_Quantum_Vacuum_Panel: n=`5` median%=`0.047775` D_eff=`8`

```powershell
python -m fsot_quantum.harder_qc
```
