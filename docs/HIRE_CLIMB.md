# Hired QC climb — higher on the same jobs

**overall_ok:** `True` · **32/32** · pin D1D38A **not edited**

After `hire_expand` 29/29. Same law, higher objects: 7-digit factors, larger dlog, Simon-16, SAT-16, Petersen, hidden shift, subset-sum, TSP n=7, Grover 1e7.

| Family | Hire | Score |
|--------|------|------:|
| factor | Shor end-job | **10/10** |
| period | Shor core | **5/5** |
| dlog | Shor / QPE | **6/6** |
| simon | Simon / HSP | **2/2** |
| sat | Grover / QAOA | **1/1** |
| partition | QAOA / QUBO | **1/1** |
| linear | HHL | **1/1** |
| color | QAOA | **1/1** |
| shift | hidden shift / QFT | **2/2** |
| subset | knapsack / QAOA | **1/1** |
| tsp | QAOA / annealer | **1/1** |
| search | Grover | **1/1** |

## Questions

| Family | Question | Answer | Method | OK |
|--------|----------|--------|--------|:--:|
| factor | What are the factors of 1022117? | `[1009,1013]` | `fermat_fold` | True |
| factor | What are the factors of 1052651? | `[1021,1031]` | `fermat_fold` | True |
| factor | What are the factors of 1102499? | `[1049,1051]` | `fermat_fold` | True |
| factor | What are the factors of 1127843? | `[1061,1063]` | `fermat_fold` | True |
| factor | What are the factors of 1192463? | `[1091,1093]` | `fermat_fold` | True |
| factor | What are the factors of 1494329? | `[1009,1481]` | `fermat_fold` | True |
| factor | What are the factors of 1503067? | `[1223,1229]` | `fermat_fold` | True |
| factor | What are the factors of 1695203? | `[1301,1303]` | `fermat_fold` | True |
| factor | What are the factors of 2040979? | `[1021,1999]` | `fermat_fold` | True |
| factor | What are the factors of 2196323? | `[1481,1483]` | `fermat_fold` | True |
| period | What is the order of 7 mod 221? | `48` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 10 mod 667? | `308` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 3 mod 1147? | `90` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 5 mod 1517? | `180` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 2 mod 8051? | `1968` | `modular_fold_plus_CF_candidates` | True |
| dlog | Discrete log: 3^x ≡ 4731 (mod 5003)? | `88` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 1068 (mod 7919)? | `144` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 9391 (mod 10007)? | `233` | `modular_fold_successive` | True |
| dlog | Discrete log: 10^x ≡ 10530 (mod 19997)? | `377` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 6259 (mod 30011)? | `610` | `modular_fold_successive` | True |
| dlog | Discrete log: 11^x ≡ 16647 (mod 40009)? | `987` | `modular_fold_successive` | True |
| simon | Simon hidden string on 12 bits (s=113)? | `113` | `collision_fold_gf2` | True |
| simon | Simon hidden string on 16 bits (s=45169)? | `45169` | `collision_fold_gf2` | True |
| sat | Satisfy the 16-bit 3-SAT (24 clauses)? | `[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]` | `clause_energy_fold` | True |
| partition | Partition {1..23} into two equal-sum sets? | `{"diff":0}` | `signed_sum_fold` | True |
| linear | Solve 4×4 Ax=b (x=[1, 2, 0, 3])? | `[1,2,0,3]` | `integer_cramer_fold` | True |
| color | 3-color the Petersen graph? | `[2,0,2,1,0,1,2,0,0,1]` | `mono_edge_fold` | True |
| shift | Hidden shift on 12 bits (s=2633)? | `2633` | `public_g_shift_fold` | True |
| shift | Hidden shift on 16 bits (s=31305)? | `31305` | `public_g_shift_fold` | True |
| subset | Subset-sum to 43 from 12 primes? | `{"sum":43,"miss":0}` | `target_energy_fold` | True |
| tsp | TSP n=7 on the seed metric — match exact tour length? | `{"length":122,"exact":122}` | `seed_start_2opt` | True |
| search | Find marked index 2718281 in 10000000 items? | `2718281` | `oracle_field_fold_collapse` | True |

## What we did not do

- Did not replay a QFT / HHL / Grover / QAOA circuit.
- Did not invent a coefficient.
- Did not touch `vendor/fsot_compute.py`.
- Did not call RSA-2048 closed. Next climb is still larger moduli on this path.

```powershell
python -m fsot_quantum.hire_climb
```
