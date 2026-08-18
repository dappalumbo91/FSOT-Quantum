# Hired QC climb 6 — 11-digit factor

**overall_ok:** `True` · **22/22** · pin D1D38A **not edited**

After `hire5`. Same modular / energy folds. Factors through **10,045,050,481**. Discrete log through **p = 4,000,037**. SAT-28, TSP n=10, 7×7 HHL, C11 independent set.

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
| factor | What are the factors of 10002200057? | `[100003,100019]` | `fermat_fold` | True |
| factor | What are the factors of 10009202107? | `[100043,100049]` | `fermat_fold` | True |
| factor | What are the factors of 10012603933? | `[100057,100069]` | `fermat_fold` | True |
| factor | What are the factors of 10021211227? | `[100103,100109]` | `fermat_fold` | True |
| factor | What are the factors of 10028019479? | `[100129,100151]` | `fermat_fold` | True |
| factor | What are the factors of 10032225857? | `[100153,100169]` | `fermat_fold` | True |
| factor | What are the factors of 10040039951? | `[100193,100207]` | `fermat_fold` | True |
| factor | What are the factors of 10045050481? | `[100213,100237]` | `fermat_fold` | True |
| factor | What are the factors of 10015400453? | `[100003,100151]` | `fermat_fold` | True |
| factor | What are the factors of 10025008901? | `[100043,100207]` | `fermat_fold` | True |
| period | What is the order of 3 mod 1022117? | `42504` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 5 mod 1052651? | `26265` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 7 mod 1102499? | `550200` | `modular_fold_plus_CF_candidates` | True |
| dlog | Discrete log: 3^x ≡ 543743 (mod 2000003)? | `610` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 1441835 (mod 2500009)? | `987` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 950239 (mod 3000017)? | `1597` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 587958 (mod 4000037)? | `2584` | `modular_fold_successive` | True |
| sat | Satisfy the 28-bit 3-SAT (56 clauses)? | `0` | `clause_energy_fold` | True |
| tsp | TSP n=10 on the seed metric — match exact tour length? | `{"length":131,"exact":131}` | `seed_start_2opt` | True |
| linear | Solve 7×7 Ax=b? | `[1,0,-1,2,1,0,1]` | `integer_cramer_fold` | True |
| mis | Max independent set of the 11-cycle? | `{"size":5,"exact":5}` | `legal_size_fold` | True |
| partition | Partition {1..35} into two equal-sum sets? | `{"diff":0}` | `signed_sum_fold` | True |

## What we did not do

- Did not open a genetics panel.
- Did not replay a QFT / HHL / QAOA circuit.
- Did not invent a coefficient.
- Did not call RSA-2048 closed.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.hire_climb6
```
