# Expand sim — Lean chemistry + more QM into this fold

**overall_ok:** `True`
**wall_s:** `0.03`

- pin chemistry: 68/68
- pin QM waves: 14/14
- Lean chemistry replay: 145/145 @0.5% (145 rows)
- Lean QM/optics/materials/vacuum: 217/217 (217 rows)

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.expand_sim
```
