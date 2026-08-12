# Quantum bleed refine — full Lean fabric, not just the 35-row core

**overall_ok:** `True`
**wall_s:** `1.39`

Quantum jobs are not stuck at one D_eff. QM/QC/QO/particle/chem/CM bleed through A_bleed·POOF·|S_i||S_j| / (1+|ΔD|/25), then relax. Same connective law as FSOT-2.1-Lean complex-system derivation.

## Plain language

Think of D_eff like which part of the machine you're turning: measurement (QM, 6), compute (QC, 11), light (optics, 11 observed), atoms, bonds, packing. They share oil — A_bleed and POOF/SUCTION. The leak between gears is κ, smaller when the gears are farther apart in D. We let S wave until it settles. We do not add a new bolt (free parameter). LLM-style weights are that extra bolt; this fold stays mechanical.

## Coupled S (this fold)

- yin–yang POOF/(POOF+SUCTION) = `0.5107`
- relax steps = `7` (round(1/POOF))
- S(QM) eq `0.9555` → coupled `0.9336`
- S(QC) eq `-0.1477` → coupled `-0.1424`
- QC job modulation (pack vs measure) = `1.000000` (I_QC_CM=1.0000, I_QM_QC=1.0000)

A modulation near 1 means the wave is small — the medium is already close to equilibrium. That is information, not a miss.

## FSOT-2.1-Lean quantum atlas (already solved there)

status=`ingested` files=`8` records=`569`

| Domain | D_eff | n | median % |
|--------|------:|--:|---------:|
| Quantum_Computing | 11 | 177 | 0.0002953462072651492 |
| Quantum_Mechanics | 6 | 50 | 9.52387420324368e-05 |
| Quantum_Optics | 6 | 50 | 9.52387420324368e-05 |
| Quantum_Information | 11 | 21 | 0.0 |
| Quantum_Mechanics_Entanglement_Depth_Panel | 16 | 21 | 0.014767 |
| Quantum_Computing_Math_Depth_Panel | 19 | 77 | 0.014767 |
| None | 16 | 168 | 0.01692529386942307 |
| Founding_Quantum_Vacuum_Panel | 8 | 5 | 0.047775 |

## Default job ledgers (unchanged claim)

- field opt exact 13/13
- chemistry 68/68 @0.5%
- QM waves 14/14 @0.5%
- G1 vs BKS 1.952856159669649%

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.bleed_refine
```

Mother repo: https://github.com/dappalumbo91/FSOT-2.1-Lean
