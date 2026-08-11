# FSOT-Quantum skeptic kit

**overall_ok:** `True`
**wall_s:** `1.889`

| Gate | OK |
|------|----|
| pin_D1D38A | True |
| fsot_lib_smoke_owned | True |
| fsot_quantum_verify | True |
| capability_suite | True |
| optimization_panel | True |
| textbook_map | True |
| scale_scoreboard | True |
| zero_free_params | True |

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.skeptic_kit
```

Kill criteria: any gate false; pin ≠ D1D38A; free-parameter introduction.
