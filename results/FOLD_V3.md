# Fold path v3 — natural steps

**overall_ok:** `True`
**wall_s:** `3.08`

## Thesis

Fold path v3: public MaxCut/Ising under cost ledger, multi-stream fold scheduler, lattice-surgery logical folds, broader chem catalog

## Panels

- **fold benchmarks:** 30/30 ok=True summary={'exact_matches': 21, 'exact_total': 21, 'ratio_floor_passes': 9, 'ratio_floor_total': 9, 'max_n': 36, 'mean_fold_over_hilbert_ratio': 4189726.362626614}
- **fold scheduler:** ok=True serial=0.354s streamed=0.075s speedup=4.736911754069796
- **lattice surgery folds:** 36/36 ok=True
- **chemistry catalog:** green=68/68 families=14 aspiration=True

## Now implemented

- MaxCut/Ising fold benchmarks + Hilbert-vs-fold cost ledger
- multi-stream CUDA fold scheduler (search/Ising/pack/scalar)
- lattice-surgery merge/split/CNOT/ZZ folds d=3/5/7
- broader chemistry formula-family catalog + 0.5% green held

## Still not claimed

- continuum FTQC lattice-surgery thresholds
- QAOA circuit-depth equivalence
- RSA-scale factoring
- full FCI/CASSCF chemistry

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.fold_v3
```
