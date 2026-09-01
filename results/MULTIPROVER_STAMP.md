# FSOT-Quantum multiprover verification stamp

**stamp:** `FSOT_QUANTUM_MULTIPROVER_OK`
**overall_ok:** `True`
**pin:** `D1D38A` (expect D1D38A)
**wall_s:** `74.90`

## Provers

| Prover | Status | OK |
|--------|--------|----|
| python_runtime | pass | True |
| lean4 | pass | True |
| coq | pass | True |
| isabelle | pass | True |
| fstar | pass | True |

## Obligations: 35

Spine: `verification/obligations/quantum_spine.json`

Living Shor/QAOA integers (Q-JOB-006–010) sit next to the tiny-N demos: far RSA-shaped `10007×1000003`, p−1 stage-2 smoothness `100003−1=2·3·7·2381`, B-lock `⌊eπ⌋·⌊π⌋=24` with RSA-2048 `B=49152`, G17/G22 under 1% as integer inequalities (champions unmatched). Coq uses binary `N` for those products (unary `nat` OOMs).

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python scripts\run_multiprover_verification.py
```

Lean: `cd formal\lean; lake build`
Coq: `cd formal\coq; coqc Trinary.v Gates.v Pack.v Domains.v Hilbert.v Fold.v Jobs.v`
Isabelle: `isabelle build -d formal/isabelle FSOT_Quantum`
F*: `fstar --cache_off formal\fstar\Jobs.fst`
