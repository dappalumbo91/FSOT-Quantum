# Hired QC climb 7 — 13-digit factor

**overall_ok:** `True` · **22/22** · pin D1D38A **not edited**

After `hire6`. Same modular / energy folds. Factors through **1,000,444,049,203**. Discrete log through **p = 8,000,009**. SAT-32, TSP n=11, 8×8 HHL, C13 independent set.

| Family | Hire | Score |
|--------|------|------:|
| factor | Shor end-job | **10/10** |
| period | Shor core | **3/3** |
| dlog | Shor / QPE | **4/4** |
| sat | Grover / QAOA | **1/1** |
| tsp | QAOA / annealer | **1/1** |
| linear | HHL | **1/1** |
| mis | QAOA | **1/1** |
| partition | QAOA / QUBO | **1/1** |

## Questions

| Family | Question | Answer | Method | OK |
|--------|----------|--------|--------|:--:|
| factor | What are the factors of 1000036000099? | `[1000003,1000033]` | `fermat_fold` | True |
| factor | What are the factors of 1000076001443? | `[1000037,1000039]` | `fermat_fold` | True |
| factor | What are the factors of 1000180008019? | `[1000081,1000099]` | `fermat_fold` | True |
| factor | What are the factors of 1000254016093? | `[1000121,1000133]` | `fermat_fold` | True |
| factor | What are the factors of 1000310024009? | `[1000151,1000159]` | `fermat_fold` | True |
| factor | What are the factors of 1000354031293? | `[1000171,1000183]` | `fermat_fold` | True |
| factor | What are the factors of 1000392038407? | `[1000193,1000199]` | `fermat_fold` | True |
| factor | What are the factors of 1000444049203? | `[1000213,1000231]` | `fermat_fold` | True |
| factor | What are the factors of 1000154000453? | `[1000003,1000151]` | `fermat_fold` | True |
| factor | What are the factors of 1000236007363? | `[1000037,1000199]` | `fermat_fold` | True |
| period | What is the order of 3 mod 10400609? | `519708` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 5 mod 10575503? | `5284500` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 7 mod 10936213? | `455400` | `modular_fold_plus_CF_candidates` | True |
| dlog | Discrete log: 3^x ≡ 2463162 (mod 5000011)? | `987` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 4161430 (mod 6000011)? | `1597` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 6741744 (mod 7000003)? | `2584` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 658015 (mod 8000009)? | `4181` | `modular_fold_successive` | True |
| sat | Satisfy the 32-bit 3-SAT (64 clauses)? | `0` | `clause_energy_fold` | True |
| tsp | TSP n=11 on the seed metric — match exact tour length? | `{"length":136,"exact":136}` | `seed_start_2opt` | True |
| linear | Solve 8×8 Ax=b? | `[1,0,-1,2,0,1,-1,2]` | `integer_cramer_fold` | True |
| mis | Max independent set of the 13-cycle? | `{"size":6,"exact":6}` | `legal_size_fold` | True |
| partition | Partition {1..39} into two equal-sum sets? | `{"diff":0}` | `signed_sum_fold` | True |

## What we did not do

- Did not replay a QFT / HHL / QAOA circuit.
- Did not invent a coefficient.
- Did not call RSA-2048 closed.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.hire_climb7
```
