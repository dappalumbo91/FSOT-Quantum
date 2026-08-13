# Paper scaffold — FSOT quantum computing pathway

**Working title:** Fluid Spacetime Omni-Theory as a GPU-native alternative to cryogenic quantum infrastructure for algorithmic *jobs*

**Author:** Damian Arthur Palumbo  
**Code:** https://github.com/dappalumbo91/FSOT-Quantum  
**Theory pin:** D1D38A ([FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean))  
**Runtime:** FSOT-GPU `fsot_lib` (vendored)

## Claim boundary (frozen)

| Claim | In scope? |
|-------|-----------|
| Seed-locked trinary ops replace free-parameter soft attention / free LR on GPU | Yes (FSOT-GPU lineage) |
| Same *jobs* as textbook QC demos (DJ class, BV secret, search, Ising/MaxCut, correlation structure) without QPU hardware | Yes — ledgers in `results/` |
| Multiprover stamp Lean·Coq·Isabelle·Python on spin/pack/gate/domain contracts | Yes — `FSOT_QUANTUM_MULTIPROVER_OK` |
| Hilbert-space unitary equivalence / fault-tolerant universal QC | **No** |
| Peer-reviewed acceptance | Process, not a code gate |

## Outline

1. **Introduction** — QC infrastructure cost; FSOT one-engine, zero free params  
2. **Background** — pin D1D38A; S=K(T1+T2+T3); trinary spins  
3. **FSOT-QC model** — domains QM/QC; collapse Θ; gates; GPU as parallel interface  
4. **Algorithms** — DJ, BV, Grover-collapse, Bell/GHZ structure, Ising/MaxCut  
5. **Scale** — large-n MaxCut bounds; pack/search throughput on consumer GPU  
6. **QAOA-style residual** — seed depth p=⌊π⌋; comparison to multi-start local  
7. **Textbook simulator comparison** — job-level, not fidelity  
8. **Formal multiprover** — Lean 4 master + Coq + Isabelle  
9. **Limitations & falsifiers** — residual green gates; adversarial DJ; n>16 approx floor  
10. **Conclusion**

Living wrap of what the code can do now: `docs/STATUS.md` (not this scaffold).

## Reproduce numbers

```powershell
git clone https://github.com/dappalumbo91/FSOT-Quantum.git
cd FSOT-Quantum
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum audit
python -m fsot_quantum harder
python -m fsot_quantum push3
python -m fsot_quantum family
python scripts\run_multiprover_verification.py
```

## Ledgers to cite

| Ledger | Path |
|--------|------|
| Wrap snapshot | `docs/STATUS.md` |
| Stale-target audit | `docs/STALE_TARGETS.md` |
| Physics + QI III | `docs/PHYSICS_QI3.md` |
| Gset family | `docs/GSET_FAMILY.md` |
| Question battery | `results/question_battery.json` |
| Large MaxCut | `results/large_maxcut.json` |
| QAOA-FSOT | `results/qaoa_fsot.json` |
| Textbook compare | `results/textbook_sim_compare.json` |
| Multiprover stamp | `results/multiprover_verification_report.json` |

## Next manuscript steps

- [ ] Freeze PRED-style prereg for next large-n MaxCut bank  
- [ ] Figures: throughput vs N; residual tables  
- [ ] Related work: QAOA, quantum annealing, classical approximate MaxCut  
- [ ] arXiv source via project arxiv-paper-pipeline skill when ready  
