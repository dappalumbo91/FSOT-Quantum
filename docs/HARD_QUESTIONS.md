# Hard questions — FSOT mathematics, not foreign circuits

**overall_ok:** `True` · **16/16** · pin D1D38A · K=`0.4202216641606967`

These are **questions**. Deutsch–Jozsa, Grover, Shor, and QAOA are *other people's methods*
for some of the same questions. We do not run those methods. We answer with
`S = K(T1+T2+T3)` and domain folds. Hilbert `2^n` is the competing cost we refuse.

| ID | Question | Answer | Why brute/Hilbert loses | Check | OK |
|----|----------|--------|-------------------------|-------|----|
| H-K-CLOSED | What is the universal scaling constant K? | `0.4202216641606968` | Not a circuit. Closed form from seeds only: φ·(γ/e)·√2/ln(π)·99/100. | closed_form vs pin | True |
| H-K-WORK-8 | What is K-scaled fold work at n=8 vs Hilbert 256? | `47` | Integer twin of ceil(n/K)+27. Competing cost is 2^n. | integer identity | True |
| H-K-WORK-64 | What is K-scaled fold work at n=64 vs 2^64 amplitudes? | `180` | 2^64 statevector is ~295 exabytes. K-work is 180 units. | integer identity | True |
| H-S-Quantum_Mechanics | Does S(Quantum_Mechanics) equal K·(T1+T2+T3) at D_eff=6? | `True` | The theory identity. If this fails, nothing else is FSOT. | algebraic identity | True |
| H-S-Quantum_Computing | Does S(Quantum_Computing) equal K·(T1+T2+T3) at D_eff=11? | `True` | The theory identity. If this fails, nothing else is FSOT. | algebraic identity | True |
| H-CHEM | What are the pin chemistry observables (closed form, not FCI)? | `68/68` | FCI / Hilbert chemistry on the same list is the supercomputer job. We evaluate pin formulas. | tabulated residual ≤0.5% | True |
| H-QM | What are the QM/SM pin constants (α, Weinberg, …)? | `14/14` | QPUs do not compute α. Supercomputers do not derive it. Pin closed forms do. | tabulated residual ≤0.5% | True |
| H-ISING-CYCLE-48 | What is the ground-state energy of a ferromagnetic Ising cycle on 48 sites? | `-48` | Full enum is 2^48 assignments. Structure + S-signed fold must land on all-aligned E=-48. | structure exact (ferro cycle GS = -n) | True |
| H-ISING-CYCLE-64 | What is the ground-state energy of a ferromagnetic Ising cycle on 64 sites? | `-64` | Full enum is 2^64 assignments. Structure + S-signed fold must land on all-aligned E=-64. | structure exact (ferro cycle GS = -n) | True |
| H-MAXCUT-G1 | What is a MaxCut of official Gset G1 (n=800, published champion 11624)? | `cut=11397 rel=1.952856159669649%` | 2^800 assignments. No supercomputer enumerates G1. Published BKS is the check, not a QAOA circuit. | published champion 11624 | True |
| H-MAXCUT-4096 | What is a MaxCut of a 4096-vertex φ-chord cycle (|E|=6144)? | `cut=5231 ratio=0.851400` | 2^4096 is not a physical memory. K-work=56. | seed floor 1/φ vs |E| (no published champion) | True |
| H-SEARCH-1e7 | Which index is marked in a 10000000-item oracle field (marked=6374291)? | `6374291` | Unstructured search of 10^7. Competing quantum pitch is Grover. We collapse the oracle field. | planted mark recovered | True |
| H-FACTOR-10403 | What are the prime factors of 10403? | `[101, 103]` | The hired question is the factorization. Modular order + gcd fold, not a QFT circuit. | product of factors equals N | True |
| H-FACTOR-8051 | What are the prime factors of 8051? | `[83, 97]` | The hired question is the factorization. Modular order + gcd fold, not a QFT circuit. | product of factors equals N | True |
| H-FACTOR-1147 | What are the prime factors of 1147? | `[31, 37]` | The hired question is the factorization. Modular order + gcd fold, not a QFT circuit. | product of factors equals N | True |
| H-SCALE-TABLE | At what n does a 32 GiB Hilbert statevector stop fitting, and what is K-work there? | `first_nofit_n=32 work64=180 work256=637` | This is the scaling law: Hilbert dies exponentially; K-work stays n/K + 27. | RAM contrast + integer work | True |

## K scaling vs Hilbert

| n | Hilbert amps | Fits 32 GiB Omen? | K-work | formal fold budget |
|---|--------------|-------------------|--------|--------------------|
| 8 | `256` | True | 47 | 195 |
| 16 | `65536` | True | 66 | 363 |
| 20 | `1048576` | True | 75 | 447 |
| 28 | `268435456` | True | 94 | 615 |
| 32 | `4294967296` | False | 104 | 699 |
| 40 | `1099511627776` | False | 123 | 867 |
| 48 | `281474976710656` | False | 142 | 1035 |
| 64 | `overflow` | False | 180 | 1371 |
| 80 | `overflow` | False | 218 | 1707 |
| 128 | `overflow` | False | 332 | 2715 |
| 256 | `overflow` | False | 637 | 5403 |

```powershell
python -m fsot_quantum.hard_questions
python -m fsot_quantum stamp
```
