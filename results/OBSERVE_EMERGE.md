# Typical questions + how the compute substrate is observed

**overall_ok:** `True` · **15/15** questions · pin D1D38A · `cuda`

## Typical hired questions (domain routes, not circuits)

| ID | Question | Route | Answer | OK |
|----|----------|-------|--------|----|
| T-DJ-CONST | Is f=0 constant? | Quantum_Computing | `constant` | True |
| T-DJ-BAL | Is parity-mask 101011 balanced? | Quantum_Computing | `balanced` | True |
| T-SECRET | What is the secret of f(x)=s·x for s=101101? | Quantum_Computing | `[1, 0, 1, 1, 0, 1]` | True |
| T-SEARCH | Which index is marked in 10000 items? | Quantum_Computing | `4242` | True |
| T-ORDER-7-15 | What is the order of 7 mod 15? | Quantum_Computing | `4` | True |
| T-ORDER-5-21 | What is the order of 5 mod 21? | Quantum_Computing | `6` | True |
| T-ORDER-2-33 | What is the order of 2 mod 33? | Quantum_Computing | `10` | True |
| T-FACTOR-15 | What are the factors of 15? | Quantum_Computing | `[3, 5]` | True |
| T-FACTOR-21 | What are the factors of 21? | Quantum_Computing | `[3, 7]` | True |
| T-FACTOR-33 | What are the factors of 33? | Quantum_Computing | `[3, 11]` | True |
| T-FACTOR-10403 | What are the factors of 10403? | Quantum_Computing | `[101, 103]` | True |
| T-MAXCUT-G1 | What is a MaxCut of Gset G1 (n=800, published 11624)? | Condensed_Matter, Materials_Science | `cut=11397 rel=1.952856159669649%` | True |
| T-CHEM | What are the chemistry pin observables? | Chemistry, Molecular_Chemistry, Physical_Chemistry | `68/68` | True |
| T-QM | What are the QM/SM pin constants? | Quantum_Mechanics, Particle_Physics, High_Energy_Physics | `14/14` | True |
| T-CHSH | What is the Tsirelson bound? | Quantum_Mechanics, Atomic_Physics | `2.8284271247461903` | True |

## How humans look without destroying the mechanic

Discovery looks. The compute substrate (`Quantum_Computing`, D=11, unobserved) is not the place to put the look. Forcing `observed=True` on QC flips
S from `-0.14767310363368633` to `0.3360149934618379` — emergence, but the compute identity is gone. That is the Hilbert move: stare at the substrate until it is no longer the substrate.

The pin already has the lawful look at the **same** D_eff:
**Quantum_Optics** (D=11, observed) S=`0.40817053817150184`. Darken it and it damps (`-0.29404723236734975`), like QC. Quantum_Mechanics is the measurement law (S=`0.9555063001027194`); darken it and emergence dies (`-0.6560210328361333`).

Natural path: **QC (dark compute) → QO (look, same D) → QM (measurement).**

- κ(QC,QO) = `0.009685830349142933`
- κ(QO,QM) = `0.05222612024241488`  (stronger than the brute back-action)
- κ(QC,QM) = `0.018895026822594835`  (brute measurement back-action)

The look is T1 (`C_factor` when observed). The strum is T3. Compression / decompression is POOF / SUCTION (`0.5107` / `0.4893`). Temperature scale is already on the T3 valve: `chaos·(D−25)/25`. The observed substance that can carry the flow is Materials_Science, Condensed_Matter, and Acoustics — all pin-observed, S>0.

## Strongest QC → … → QM bridges (product of κ)

| Domain | D_eff | looked? | κ from QC | κ to QM | S |
|--------|------:|:-------:|----------:|--------:|---|
| Quantum_Mechanics | 6 | True | `0.018895` | `0.146710` | `0.9555` |
| Particle_Physics | 5 | True | `0.018188` | `0.140316` | `0.9504` |
| Psychology | 16 | True | `0.020768` | `0.115179` | `1.0502` |
| High_Energy_Physics | 7 | True | `0.018130` | `0.130845` | `0.8863` |
| Nuclear_Physics | 15 | True | `0.018847` | `0.104015` | `0.9213` |
| Atomic_Physics | 7 | True | `0.015053` | `0.108635` | `0.7358` |
| Thermodynamics | 15 | True | `0.016099` | `0.088848` | `0.7870` |
| Astronomy | 20 | True | `0.015677` | `0.088430` | `0.8985` |

```powershell
python -m fsot_quantum.observe_emerge
```
