# Reproduce — FSOT-Quantum

**Pin:** D1D38A  
**Python:** 3.11+  
**Optional:** CUDA (torch), lake, coqc, Isabelle, fstar, Zig, QEMU

What the numbers mean: [`STATUS.md`](STATUS.md) · what we can claim: [`CLAIMS.md`](CLAIMS.md) · rung order: [`LADDER.md`](LADDER.md) · doc map: [`INDEX.md`](INDEX.md)

```powershell
cd <clone>
$env:PYTHONPATH = (Get-Location).Path
pip install -r requirements.txt   # torch optional; pin checks run without it
```

## Wrap check (stranger path)

```powershell
python -m fsot_quantum check
python -m fsot_quantum audit       # expect 20/20
python -m fsot_quantum harder      # expect 20/20
python -m fsot_quantum push3       # expect 41/41
python -m fsot_quantum family      # 10/11 under 1%; G17 is 1.017%
python -m fsot_quantum open        # diagnosis only (wrong-object 6% scores)
python -m fsot_quantum vcb         # inclusive 0.002% · exclusive B→D 0.15%
python -m fsot_quantum h0          # Planck 0.024% · SH0ES 1.00%
python -m fsot_quantum contested   # Lean contested sectors
python -m fsot_quantum leftovers   # remaining opens
python -m fsot_quantum hire        # factor / dlog / Simon / SAT / HHL 29/29
python -m fsot_quantum hire2       # 7-digit factor / Simon-16 / SAT-16 / TSP 32/32
python -m fsot_quantum branch      # probability as \|S\| branching 19/19
python -m fsot_quantum formulas    # formula list
python -m fsot_quantum stamp       # Lean · Coq · Isabelle · F* · Python
```

## Required (no extra provers)

```powershell
python -m fsot_quantum check      # pin vs Lean clone if _ref present
python -m fsot_lib.smoke_owned
python -m fsot_quantum.verify
python -m fsot_quantum.forward    # known published answers
python -m fsot_quantum.harder     # CKM / Ising / nuclear / Gset
python -m fsot_quantum.physics_qi # 3D Ising / XY / Heisenberg / g-2 / Lean QI
python -m fsot_quantum.physics_qi2 # Higgs/Z, nuclear, cosmology, Casimir, CHSH
python -m fsot_quantum.stale_targets
python -m fsot_quantum.physics_qi3 # leftover CKM / LEP / BBN / cosmology
python -m fsot_quantum.gset_family
python -m fsot_quantum.open_objects
python -m fsot_quantum.vcb_puzzle
python -m fsot_quantum.h0_tension
python -m fsot_quantum.contested_sectors
python -m fsot_quantum.open_remaining
python -m fsot_quantum.hire_expand
python -m fsot_quantum.hire_climb
python -m fsot_quantum.probability_branch
python -m fsot_quantum.formula_catalog
python -m fsot_quantum stamp
python -m fsot_quantum.organ_export
# BR(H→gg) vs YR4 (not the stale 0.0785 in vendor wave8): docs/BR_H_GG.md
# Three earlier audit misses were wrong objects: docs/MISS_THREE.md
# Wrap snapshot: docs/STATUS.md
```

Gset G1 ships in `data/gset/G1.txt`. G14/G22 fetch from Stanford Ye when `FSOT_FETCH_GSET` is not `0`.

If MaxCut residuals look wrong, run the diagnosis (why 1-opt plateaus):

```powershell
python -m fsot_quantum.gset_diagnose
```

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
