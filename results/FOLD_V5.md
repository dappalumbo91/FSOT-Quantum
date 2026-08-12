# Fold path v5 — leftovers

**overall_ok:** `True`
**wall_s:** `14.86`

## Thesis

Hit leftover rungs honestly: official Gset if present, multi-GPU inventory+shards, adder/QFT-role folds, QEMU fold kernel, paper note

## Panels

- **Gset official:** status=skip_official_parser_ok parser=True found=False pass=0/0
- **multi-GPU:** n_gpu=1 ['NVIDIA GeForce RTX 5070'] shards=4/4 claimed_speedup=False
- **logical algos:** 38/38 ok=True
- **QEMU fold gate:** pass fold=True cnotfold=True kernel=True
- **paper note:** ok=True `papers\02-fold-not-hilbert\NOTE.md`

## Now implemented

- Gset official loader + parser fixture (skip if no archive)
- multi-GPU inventory + shard runner (honest n_gpu=1 on this host)
- ripple-carry adder + QFT-role bit-reversal/phase folds
- QEMU serial gate for fold + cnotfold kernel tests
- papers/02-fold-not-hilbert/NOTE.md

## Still not claimed

- G1–G54 published residual table without local/official files
- multi-GPU speedup on a 1-GPU machine
- Hilbert QFT/adder circuit equivalence

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.fold_v5
```
