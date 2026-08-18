# Hired QC questions — answered on this fold

**overall_ok:** `True` · **29/29** · pin D1D38A **not edited**

These are the *questions* people hire a QPU for. Answered with modular folds, collapse, and seed starts. No foreign circuit. No new coefficient. Factor ladder starts after harder-QC 10403.

| Family | Hire | Score |
|--------|------|------:|
| factor | Shor end-job | **10/10** |
| dlog | Shor / QPE | **10/10** |
| simon | Simon / HSP | **1/1** |
| sat | Grover / QAOA | **1/1** |
| partition | QAOA / QUBO | **1/1** |
| linear | HHL | **3/3** |
| color | QAOA | **1/1** |
| search | Grover | **2/2** |

## Questions

| Family | Question | Answer | Method | OK |
|--------|----------|--------|--------|:--:|
| factor | What are the factors of 11413? | `[101,113]` | `gcd_fold` | True |
| factor | What are the factors of 16637? | `[127,131]` | `fermat_fold` | True |
| factor | What are the factors of 19043? | `[137,139]` | `fermat_fold` | True |
| factor | What are the factors of 25591? | `[157,163]` | `fermat_fold` | True |
| factor | What are the factors of 39203? | `[197,199]` | `gcd_fold` | True |
| factor | What are the factors of 50621? | `[223,227]` | `fermat_fold` | True |
| factor | What are the factors of 64507? | `[251,257]` | `gcd_fold` | True |
| factor | What are the factors of 103603? | `[313,331]` | `fermat_fold` | True |
| factor | What are the factors of 142763? | `[367,389]` | `fermat_fold` | True |
| factor | What are the factors of 172189? | `[409,421]` | `fermat_fold` | True |
| dlog | Discrete log: 3^x ≡ 13 (mod 17)? | `4` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 8 (mod 23)? | `6` | `modular_fold_successive` | True |
| dlog | Discrete log: 2^x ≡ 3 (mod 29)? | `5` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 4 (mod 71)? | `12` | `modular_fold_successive` | True |
| dlog | Discrete log: 3^x ≡ 73 (mod 101)? | `69` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 82 (mod 107)? | `17` | `modular_fold_successive` | True |
| dlog | Discrete log: 10^x ≡ 94 (mod 251)? | `8` | `modular_fold_successive` | True |
| dlog | Discrete log: 3^x ≡ 52 (mod 503)? | `42` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 338 (mod 1009)? | `88` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 127 (mod 2053)? | `119` | `modular_fold_successive` | True |
| simon | Simon hidden string on 8 bits (s=113)? | `113` | `collision_fold_gf2` | True |
| sat | Satisfy the 8-bit 3-SAT (10 clauses)? | `[1,0,0,0,0,0,0,0]` | `clause_energy_fold` | True |
| partition | Partition {1..15} into two equal-sum sets? | `{"diff":0,"spins":[-1,-1,-1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1]}` | `signed_sum_fold` | True |
| linear | Solve Ax=b for A=[[2, 1], [1, 3]] b=[5, 10]? | `[1,3]` | `integer_cramer_fold` | True |
| linear | Solve Ax=b for A=[[3, 0, 1], [1, 2, 0], [0, 1, 4]] b=[9, 4, 13]? | `[2,1,3]` | `integer_cramer_fold` | True |
| linear | Solve Ax=b for A=[[4, 1, 0], [1, 3, 1], [0, 1, 2]] b=[9, 8, 7]? | `[2,1,3]` | `integer_cramer_fold` | True |
| color | 3-color the 5-cycle? | `[1,2,1,2,0]` | `mono_edge_fold` | True |
| search | Find marked index 42424 in 100000 items? | `42424` | `oracle_field_fold_collapse` | True |
| search | Find marked index 314159 in 1000000 items? | `314159` | `oracle_field_fold_collapse` | True |

## What we did not do

- Did not replay a QFT / HHL / Grover / QAOA circuit.
- Did not invent a coefficient or a learning rate.
- Did not touch `vendor/fsot_compute.py`.
- Did not call RSA-2048 closed. Larger moduli stay the next climb on this path.

```powershell
python -m fsot_quantum.hire_expand
```
