# Quantum computing questions — answers from this fold

**overall_ok:** `True` · **19/19** · pin D1D38A

| ID | Question | Answer | OK |
|----|----------|--------|----|
| Q-DJ-CONST | Is f=0 constant on 6 bits? (DJ role) | `constant` | True |
| Q-DJ-BAL | Is parity-mask 101011 balanced? (DJ role) | `balanced` | True |
| Q-BV | What is the secret of f(x)=s·x for s=101101? | `[1, 0, 1, 1, 0, 1]` | True |
| Q-GROVER | Find the marked index in 10000 items (marked=4242). | `4242` | True |
| Q-PERIOD-7-15 | What is the order of 7 mod 15? | `4` | True |
| Q-PERIOD-5-21 | What is the order of 5 mod 21? | `6` | True |
| Q-PERIOD-2-33 | What is the order of 2 mod 33? | `10` | True |
| Q-PERIOD-8-51 | What is the order of 8 mod 51? | `8` | True |
| Q-FACTOR-15 | Factor the composite 15. | `[3, 5]` | True |
| Q-FACTOR-21 | Factor the composite 21. | `[3, 7]` | True |
| Q-FACTOR-33 | Factor the composite 33. | `[3, 11]` | True |
| Q-ISING-BANK | Do collapse+consensus field solves match exact Ising/MaxCut (n<=12 bank)? | `13/13` | True |
| Q-MAXCUT-G1 | Official Gset G1 (n=800): fold cut vs published 11624 — within 5%? | `cut=11397 rel=1.952856159669649%` | True |
| Q-CHEM | Pin chemistry observables inside 0.5%? | `68/68` | True |
| Q-QM-CONST | QM/SM pin constants (alpha, Weinberg, …) inside 0.5%? | `14/14` | True |
| Q-S-QM | Is S(QM) emergence (>0)? | `True` | True |
| Q-S-QC | Is S(QC) damping (<0)? | `True` | True |
| Q-CHSH | What is the Tsirelson bound (seed 2√2)? | `2.8284271247461903` | True |
| Q-FOLD-COST | Is foldBudget(8)=195 < 256? | `True` | True |


## Formal twins (same integer facts)

| Prover | File |
|--------|------|
| Lean 4 | `formal/lean/FSOTQuantumFormal/Jobs.lean` |
| Coq | `formal/coq/Jobs.v` |
| Isabelle/HOL | `formal/isabelle/Jobs.thy` |
| F* | `formal/fstar/Jobs.fst` |

Shared surface: `7^4 ≡ 1 (mod 15)`, `5^6 ≡ 1 (mod 21)`, `2^10 ≡ 1 (mod 33)`,
`8^8 ≡ 1 (mod 51)`, `15=3·5`, `21=3·7`, `33=3·11`, `foldBudget(8)=195<256`.

Cross-stamp: `python scripts/run_multiprover_verification.py`

## Last multiprover stamp

# FSOT-Quantum multiprover verification stamp

**stamp:** `FSOT_QUANTUM_MULTIPROVER_OK`
**overall_ok:** `True`
**pin:** `D1D38A` (expect D1D38A)
**wall_s:** `59.91`

## Provers

| Prover | Status | OK |
|--------|--------|----|
| python_runtime | pass | True |
| lean4 | pass | True |
| coq | pass | True |
| isabelle | pass | True |
| fstar | pass | True |

## Obligations: 23

Spine: `verification/obligations/quantum_spine.json`

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


```powershell
python -m fsot_quantum.ask_qc
python scripts\run_multiprover_verification.py
```
