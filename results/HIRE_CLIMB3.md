# Hired QC climb 3 — 8-digit factors

**overall_ok:** `True` · **17/17** · pin D1D38A **not edited**

After `hire2` (7-digit). Same modular fold. Factors through **20,937,233**. Discrete log through **p = 100003**.

| Family | Hire | Score |
|--------|------|------:|
| factor | Shor end-job | **10/10** |
| period | Shor core | **3/3** |
| dlog | Shor / QPE | **4/4** |

## Questions

| Family | Question | Answer | Method | OK |
|--------|----------|--------|--------|:--:|
| factor | What are the factors of 10400609? | `[3221, 3229]` | `fermat_fold` | True |
| factor | What are the factors of 10575503? | `[3251, 3253]` | `fermat_fold` | True |
| factor | What are the factors of 10936213? | `[3301, 3313]` | `fermat_fold` | True |
| factor | What are the factors of 12006221? | `[3463, 3467]` | `fermat_fold` | True |
| factor | What are the factors of 12348187? | `[3511, 3517]` | `fermat_fold` | True |
| factor | What are the factors of 12787751? | `[3571, 3581]` | `fermat_fold` | True |
| factor | What are the factors of 16016003? | `[4001, 4003]` | `fermat_fold` | True |
| factor | What are the factors of 17040383? | `[4127, 4129]` | `fermat_fold` | True |
| factor | What are the factors of 16114663? | `[3221, 5003]` | `fermat_fold` | True |
| factor | What are the factors of 20937233? | `[4001, 5233]` | `fermat_fold` | True |
| period | What is the order of 3 mod 10403? | `1700` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 5 mod 6557? | `3198` | `modular_fold_plus_CF_candidates` | True |
| period | What is the order of 10 mod 8633? | `1056` | `modular_fold_plus_CF_candidates` | True |
| dlog | Discrete log: 3^x ≡ 47501 (mod 50021)? | `144` | `modular_fold_successive` | True |
| dlog | Discrete log: 5^x ≡ 35997 (mod 70001)? | `233` | `modular_fold_successive` | True |
| dlog | Discrete log: 6^x ≡ 87447 (mod 90001)? | `377` | `modular_fold_successive` | True |
| dlog | Discrete log: 7^x ≡ 72842 (mod 100003)? | `610` | `modular_fold_successive` | True |

## What we did not do

- Did not replay a QFT circuit.
- Did not invent a coefficient.
- Did not call RSA-2048 closed.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.hire_climb3
```
