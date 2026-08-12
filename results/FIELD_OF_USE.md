# Field of use — honest FSOT on QM/QC jobs

**overall_ok:** `True`
**wall_s:** `1.37`

Apply FSOT mathematics (Θ collapse, consensus, D_eff / S, pin formulas) to QM/QC *jobs*. Label theater. Do not sell 2^n bridges as the path.

## Classification

| Job | Industry pitch | FSOT math | Class |
|-----|----------------|-----------|-------|
| chemistry observables | quantum chemistry / FCI sales pitch | pin seed formulas + formula-family fold (π−θ_s) | **applied_fsot** |
| QM / SM constants (α, Weinberg, mass ratios) | precision QM / particle data | vendor pin expressions vs measured | **applied_fsot** |
| marked search | Grover | collapse through Θ on oracle field | **applied_fsot** |
| Ising / MaxCut | QAOA / annealer | h_i=Σ J s_j → collapse + consensus + domain S | **applied_fsot** |
| period / factor (tiny N) | Shor | modular order + collapse over candidate scores | **applied_fsot** |
| phase class | QPE | S(D_eff) emergence/damping | **applied_fsot** |
| bit-reversal 'QFT-role' | QFT | none — bit reverse is not a QFT | **theater_do_not_claim** |
| Hilbert H/CX/QFT fragments | circuit sim | seed π angles only; still 2^n amps | **optional_bridge** |

## Live panels

- **field Ising/MaxCut:** 13/13 exact 13/13
- **QM pin waves:** green 14/14 5% 14/14 median=0.002173459608308579
- **chemistry fold:** 68/68 @0.5%
- **Gset official:** official 1/1
- **collapse search:** True
- **period/factor:** 3/3 / 4/4
- **S(QM), S(QC):** 0.9555, -0.1477

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.field_of_use
```
