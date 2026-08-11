# Fold path v2 — natural steps

**overall_ok:** `True`
**wall_s:** `1.98`

## Thesis

Next natural steps on fold path: chemistry residual folds, GPU fold job queue, surface+phase folds — still not Hilbert 2^n

## Panels

- **chemistry fold:** ok=True 0.5% base 67/68 → fold 68/68 aspiration=True
- **GPU fold queue:** ok=True gpu=NVIDIA GeForce RTX 5070 highlights={'jobs_ok': '9/9', 'max_search_ips': 263130.82591716695, 'max_ising_ips': 27372.726189351826, 'max_pack_trits_per_sec': 3234716593.5778975, 'max_scalar_per_sec': 2480817.0779685243, 'peak_mem_mb': 4213.17626953125, 'complexity_weight': 0.6180339887498949, 'fold_depth': {'shallow': 1, 'mid': 3, 'deep': 4, 'meta': 8}}
- **surface+phase folds:** 13/13 ok=True
- **fold jobs v1:** 27/27 ok=True

## Cost contrast (n=32)

- Hilbert amps: `4294967296`
- Fold budget: `621`
- Ratio: ~`6916211×`

## Now implemented

- chemistry formula-family fold: π⁵·φ → π⁵·φ+(π−θ_s) (0.5% aspiration)
- GPU fold queue: search/modular/Ising/pack/D_eff scalars
- surface bit+phase nested CSS folds d=3/5/7
- phase class via D_eff + surface distance (no QPE Hilbert)

## Still not claimed

- full molecular FCI/CASSCF
- device-scale FTQC thresholds
- RSA-scale factoring
- Hilbert-universal unitary simulation

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.fold_v2
```
