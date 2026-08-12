# Fold path v4 — natural steps

**overall_ok:** `True`
**wall_s:** `7.64`

## Thesis

Fold v4: multi-process scheduler, teleportation sequences, Gset-style MaxCut ledger, fold-vs-Hilbert formal cost, Zig twin

## Panels

- **mp scheduler:** ok=True workers=4 serial=1.241s pool=1.939772300000186 speedup=0.6399404198137201
- **teleport sequences:** 30/30 ok=True
- **Gset-style MaxCut:** 4/4 ok=True
- **formal fold cost (Python):** pass
- **Zig fold twin:** pass

## Fold vs Hilbert (formal integer proxy)

| n | foldBudget | 2^n |
|--:|-----------:|----:|
| 8 | 195 | 256 |
| 16 | 363 | 65536 |
| 20 | 447 | 1048576 |
| 32 | 699 | 4294967296 |

## Now implemented

- multi-process fold scheduler (search/period/factor/Ising)
- lattice-surgery SWAP / copy / GHZ-class / A→B→C teleport chain
- Gset-style MaxCut n=40..100 under 1/φ floor + cost ledger
- foldBudget vs 2^n lemmas (Lean/Coq/Isabelle + Python + Zig)

## Still not claimed

- downloaded official Gset archive residuals
- continuum FTQC teleportation thresholds
- multi-GPU distributed fold (this is multi-process on one host)

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.fold_v4
python scripts\run_multiprover_verification.py
```
