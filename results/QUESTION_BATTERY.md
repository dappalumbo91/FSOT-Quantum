# FSOT-QC Question Battery

**overall:** 224/224 (100.00%)
**device:** `cuda`
**wall_s:** `1.606`

## By category

| Category | Pass | Total | Accuracy |
|----------|-----:|------:|---------:|
| bernstein_vazirani | 50 | 50 | 100.0% |
| deutsch_jozsa | 42 | 42 | 100.0% |
| deutsch_jozsa_adversarial | 2 | 2 | 100.0% |
| entanglement | 2 | 2 | 100.0% |
| gates | 6 | 6 | 100.0% |
| grover_batch_gpu | 3 | 3 | 100.0% |
| grover_search | 72 | 72 | 100.0% |
| measurement | 6 | 6 | 100.0% |
| optimization_bank | 13 | 13 | 100.0% |
| optimization_random | 25 | 25 | 100.0% |
| phase_class | 3 | 3 | 100.0% |

## Failures (refine targets)

_None — full pass._

## Refine priority

_No category below 100%._

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.question_battery
```
