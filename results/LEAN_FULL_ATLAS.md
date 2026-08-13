# Full Lean atlas — everything solved, not just chemistry

**overall_ok:** `True`
**wall_s:** `1.33`

- files parsed: **473/473**
- named domains: **432**
- headline records (sum): **2346836**
- material rows replayed (capped): **13228**
- replay-fail files: **0**

This is the mother fabric (FSOT-2.1-Lean) pulled into the QC fold as a ledger.

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.lean_full_atlas
```
