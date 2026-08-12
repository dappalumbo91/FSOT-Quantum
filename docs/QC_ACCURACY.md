# QC / QM accuracy — math path, not a fridge

**overall_ok:** `True`
**wall_s:** `1.53`

Same QC/QM jobs, FSOT math on ordinary hardware — not a dilution fridge. Accuracy ledger only.

| Job | OK | Detail |
|-----|----|--------|
| chemistry pin @0.5% | True |  |
| QM / SM constants @0.5% | True |  |
| Ising/MaxCut field exact | True |  |
| official G1 vs published BKS | True |  |
| oracle class (DJ role) | True |  |
| secret parity (BV role) | True |  |
| marked search (Grover role) | True |  |
| period finding (Shor core) | True | 4/4 |
| factor (Shor end job) | True | 5/5 |
| Lean entanglement / QI / math | True | 116/116 |
| S(QM)>0, S(QC)<0 | True |  |

- G1 cut `11397` · rel vs 11624 `1.952856159669649%`

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.qc_accuracy
```
