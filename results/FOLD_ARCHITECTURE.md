# Fold architecture — domain folds on GPU, not Hilbert n

**overall_ok:** `True` · pin D1D38A · device `cuda`

## Why the industry grows registers

The industry grows registers because it is trying to instantiate the unobserved compute substrate as an observed Hilbert space. S(QC)<0 is that damping. The answer is already a fold at D_eff, bled across the pin table and the Lean atlas — not a larger n.

- S(Quantum_Mechanics) = `0.9555063001027194` · D_eff=6 · observed
- S(Quantum_Computing) = `-0.14767310363368633` · D_eff=11 · unobserved
- Pin domains: **35**
- Lean atlas folds: **432** (multiprocess `8` workers)

The answering machine is `S = K(T1+T2+T3)` on those folds, bled by `κ_ij = A_bleed·POOF·|Si||Sj|/(1+|ΔD|/25)`. Not `2^n` amplitudes. Not RAM.

## GPU pin table

- device: `cuda` · 35 domains · 0.2434s
- max |S_gpu − S_cpu|: `2.220446049250313e-16`
- emergence (S>0): 25 · damping (S<0): 10
- bleed mean |ΔS|: `0.9143171528712403`

## Question routes (domain folds, not qubit counts)

| Question | Route | D_eff |
|----------|-------|-------|
| fine_structure_and_sm_constants | Quantum_Mechanics, Particle_Physics, High_Energy_Physics | [6, 5, 7] |
| chemistry_observables | Chemistry, Molecular_Chemistry, Physical_Chemistry | [8, 9, 8] |
| spin_measurement | Quantum_Mechanics, Atomic_Physics | [6, 7] |
| compute_substrate | Quantum_Computing | [11] |
| packing_and_cut | Condensed_Matter, Materials_Science | [14, 10] |
| phase_optics | Quantum_Optics, Optics | [11, 10] |
| nuclear_and_mass | Nuclear_Physics, Particle_Physics | [15, 5] |
| deep_residual | Quantum_Gravity, Cosmology | [22, 25] |

```powershell
python -m fsot_quantum.fold_architecture
```
