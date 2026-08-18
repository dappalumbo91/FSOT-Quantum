# Hired QC climb 4 — back on the QPU jobs

**overall_ok:** `True` · **22/22** · pin D1D38A **not edited**

Genetics was a side path. This rung is the jobs a QPU is hired for: 9-digit factor, larger dlog, SAT-20, TSP n=8, 5×5 HHL, C7 independent set.

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
| factor | What are the factors of 100440259? | `[10007,10037]` | `fermat_fold` | True |
| factor | What are the factors of 102151433? | `[10103,10111]` | `fermat_fold` | True |
| factor | What are the factors of 104387053? | `[10211,10223]` | `fermat_fold` | True |
| factor | What are the factors of 106131203? | `[10301,10303]` | `fermat_fold` | True |
| factor | What are the factors of 108743183? | `[10427,10429]` | `fermat_fold` | True |
| factor | What are the factors of 110397013? | `[10501,10513]` | `fermat_fold` | True |
| factor | What are the factors of 121330081? | `[11003,11027]` | `fermat_fold` | True |
| factor | What are the factors of 123543221? | `[11113,11117]` | `fermat_fold` | True |
| factor | What are the factors of 130101007? | `[10007,13001]` | `fermat_fold` | True |
| factor | What are the factors of 144216077? | `[12007,12011]` | `fermat_fold` | True |
| period | What is the order of 3 mod 39203? | `19404` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 7 mod 64507? | `32000` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 10 mod 103603? | `17160` | `modular_fold_plus_CF_candidates` | True |
| dlog | Discrete log: 3^x ≡ 107175 (mod 200003)? | `233` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 76070 (mod 250007)? | `377` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 211236 (mod 300007)? | `610` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 179126 (mod 350003)? | `987` | `modular_fold_successive` | True |
| sat | Satisfy the 20-bit 3-SAT (36 clauses)? | `0` | `clause_energy_fold` | True |
| tsp | TSP n=8 on the seed metric — match exact tour length? | `{"length":122,"exact":122}` | `seed_start_2opt` | True |
| linear | Solve 5×5 Ax=b? | `[1,0,2,-1,3]` | `integer_cramer_fold` | True |
| mis | Max independent set of the 7-cycle? | `{"size":3,"exact":3}` | `legal_size_fold` | True |
| partition | Partition {1..27} into two equal-sum sets? | `{"diff":0}` | `signed_sum_fold` | True |

## What we did not do

- Did not open another genetics panel.
- Did not replay a QFT / HHL / QAOA circuit.
- Did not invent a coefficient.
- Did not call RSA-2048 closed.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.hire_climb4
```
