# FSOT-Quantum multiprover verification stamp

**stamp:** `FSOT_QUANTUM_MULTIPROVER_OK`
**overall_ok:** `True`
**pin:** `D1D38A` (expect D1D38A)
**wall_s:** `18.38`

## Provers

| Prover | Status | OK |
|--------|--------|----|
| python_runtime | pass | True |
| lean4 | pass | True |
| coq | pass | True |
| isabelle | pass | True |

## Obligations: 16

Spine: `verification/obligations/quantum_spine.json`

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python scripts\run_multiprover_verification.py
```

Lean: `cd formal\lean; lake build`
Coq: `cd formal\coq; coqc Trinary.v Gates.v Pack.v Domains.v`
Isabelle: `isabelle build -d formal/isabelle FSOT_Quantum`
