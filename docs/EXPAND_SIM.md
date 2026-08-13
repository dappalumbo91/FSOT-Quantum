# Expand sim — Lean chemistry + more QM into this fold

**overall_ok:** `True`
**wall_s:** `0.04`

- pin chemistry: 68/68
- pin QM waves: 14/14
- Lean chemistry replay: 565/565 @0.5% (565 rows)
- Lean QM/optics/materials/vacuum: 265/265 (265 rows)

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.expand_sim
```
