# Fold versus Hilbert dimension — paper-facing cost note

**Pin:** D1D38A  
**Repo:** [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum)  
**Claim type:** *proved* (integer cost lemmas, machine-checked) + *numerically verified* (fold job suites)

This is a **technical note**, not a full arXiv monograph. It states one sharp contrast:

> Industry-style simulation of QC *jobs* expands amplitudes in \(\mathbb{C}^{2^n}\) (Hilbert dimension).  
> FSOT answers the same *job questions* by **domain folds** whose integer budget is linear in \(n\), and this inequality is checked in Lean 4, Coq, Isabelle/HOL, Python, and Zig.

## Proved (multiprover)

Integer proxy shared across provers (`fold_budget_formal`):

\[
\mathrm{foldBudget}(n) = 3\cdot n\cdot 7 + 27, \qquad \mathrm{hilbertAmps}(n) = 2^n.
\]

Checked lemmas (`Q-FOLD-001`, `Q-FOLD-002`):

| \(n\) | foldBudget | \(2^n\) | fold \(<\) Hilbert |
|------:|-----------:|--------:|:------------------:|
| 8 | 195 | 256 | yes |
| 16 | 363 | 65 536 | yes |
| 20 | 447 | 1 048 576 | yes |
| 32 | 699 | 4 294 967 296 | yes |

Reproduce:

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python scripts\run_multiprover_verification.py
```

Sources: `formal/lean/FSOTQuantumFormal/Fold.lean`, `formal/coq/Fold.v`, `formal/isabelle/Fold.thy`, `fsot_quantum/fold_complexity.py`.

## What is *not* claimed

- Query-complexity superiority vs quantum in every oracle model  
- RSA-scale factoring  
- Device-scale FTQC thresholds  
- That every QC circuit has a poly-size fold twin  

The inequality is a **cost-geometry** statement: when the job admits modular / consensus / domain-fold structure, one need not allocate \(2^n\) amplitudes.

## Numerically verified (same jobs)

Official Gset **G1** (Stanford/Ye, n=800, m=19176): fold cut **11397** vs published champion **11624** (rel **1.95%**, within 5% band). Hilbert QAOA on 800 qubits is not simulated.

Fold suites on this lineage (see `results/FOLD_V4.md`–`results/FOLD_V6.md`):

- Oracle class, secret, search, period, factor, Ising  
- Surface / lattice-surgery / teleport / adder sequences  
- GPU fold queue and (when present) multi-GPU shards  
- Chemistry 68/68 @ 0.5% via formula-family fold, not a free coefficient  

## How to read this

| Layer | Status |
|-------|--------|
| Cost lemmas foldBudget \(< 2^n\) at fixed \(n\) | **Proved** (4 provers + Zig) |
| Same QC *job questions* via folds | **Numerically verified** ledgers |
| “FSOT replaces quantum hardware for all tasks” | **Not claimed** |

## Related living ledgers

- `docs/FOLD_NOT_HILBERT.md`  
- `docs/FOLD_V4.md` / `docs/FOLD_V5.md`  
- `results/MULTIPROVER_STAMP.md`
