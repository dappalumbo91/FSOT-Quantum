# Reproduce — FSOT-Quantum

**Pin:** D1D38A  
**Python:** 3.11+  
**Optional:** CUDA (torch), lake, coqc, Isabelle, fstar, Zig, QEMU

```powershell
cd <clone>
$env:PYTHONPATH = (Get-Location).Path
pip install -r requirements.txt   # torch optional; pin checks run without it
```

## Required (no extra provers)

```powershell
python -m fsot_quantum check      # pin vs Lean clone if _ref present
python -m fsot_lib.smoke_owned
python -m fsot_quantum.verify
python -m fsot_quantum.forward    # known published answers
python -m fsot_quantum.harder     # CKM / Ising / nuclear / Gset
```

Gset G1 ships in `data/gset/G1.txt`. G14/G22 fetch from Stanford Ye when `FSOT_FETCH_GSET` is not `0`.

## Fold architecture + mind (GPU if present)

```powershell
python -m fsot_quantum fold       # 35 pin domains + Lean atlas
python -m fsot_quantum observe    # look path + typical questions
python -m fsot_quantum mind       # C_factor / Neuro / Psych
```

Atlas 432 needs `_ref/FSOT-2.1-Lean` (dev clone, gitignored). Without it, fold reports skip on atlas and still scores the 35 pin domains.

## Multiprover stamp

```powershell
python -m fsot_quantum stamp
```

Needs `lake`, `coqc`, Isabelle home, `fstar` on PATH for a full five-prover OK. Python runtime + pin still run if a prover is missing (that prover **skips**).

## Metal (optional)

```powershell
.\run_qemu.ps1
```

## What must not happen

- Pin prefix ≠ `D1D38A` without an announced new pin
- A new fitted coefficient
- Silent widening of a residual band
- Selling Gset MaxCut as closed while rel ≥ 1% (see `docs/LADDER.md`)

## Ledgers

Every command writes `results/<NAME>.md` and `docs/<NAME>.md` when it is a panel. Compare those files to a fresh run. The JSON twins are under `results/`.
