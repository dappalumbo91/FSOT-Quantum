# Hired QC climb 5 — 10-digit factor

**overall_ok:** `True` · **22/22** · pin D1D38A **not edited**

After `hire4`. Same modular / energy folds. Factors through **1,445,900,429**. Discrete log through **p = 1,200,007**. SAT-24, TSP n=9, 6×6 HHL, C9 independent set.

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
| factor | What are the factors of 1000773161? | `[31627,31643]` | `fermat_fold` | True |
| factor | What are the factors of 1003305481? | `[31663,31687]` | `fermat_fold` | True |
| factor | What are the factors of 1024384027? | `[32003,32009]` | `fermat_fold` | True |
| factor | What are the factors of 1090188299? | `[33013,33023]` | `fermat_fold` | True |
| factor | What are the factors of 1226750621? | `[35023,35027]` | `fermat_fold` | True |
| factor | What are the factors of 1296648077? | `[36007,36011]` | `fermat_fold` | True |
| factor | What are the factors of 1370184247? | `[37013,37019]` | `fermat_fold` | True |
| factor | What are the factors of 1445900429? | `[38011,38039]` | `fermat_fold` | True |
| factor | What are the factors of 1107798929? | `[31627,35027]` | `fermat_fold` | True |
| factor | What are the factors of 1184719057? | `[32003,37019]` | `fermat_fold` | True |
| period | What is the order of 3 mod 172189? | `7140` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 5 mod 103603? | `1320` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 7 mod 142763? | `5917` | `modular_fold_plus_CF_candidates` | True |
| dlog | Discrete log: 3^x ≡ 352380 (mod 500009)? | `377` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 555787 (mod 700001)? | `610` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 168347 (mod 1000003)? | `987` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 944385 (mod 1200007)? | `1597` | `modular_fold_successive` | True |
| sat | Satisfy the 24-bit 3-SAT (48 clauses)? | `0` | `clause_energy_fold` | True |
| tsp | TSP n=9 on the seed metric — match exact tour length? | `{"length":130,"exact":130}` | `seed_start_2opt` | True |
| linear | Solve 6×6 Ax=b? | `[1,-1,2,0,1,2]` | `integer_cramer_fold` | True |
| mis | Max independent set of the 9-cycle? | `{"size":4,"exact":4}` | `legal_size_fold` | True |
| partition | Partition {1..31} into two equal-sum sets? | `{"diff":0}` | `signed_sum_fold` | True |

## What we did not do

- Did not open a genetics panel.
- Did not replay a QFT / HHL / QAOA circuit.
- Did not invent a coefficient.
- Did not call RSA-2048 closed.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.hire_climb5
```
