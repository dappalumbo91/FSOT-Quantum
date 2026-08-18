# Heights next — close G17, log-N factor

**G17:** cut `3034` vs 3047 · **0.426649163111257%** · 13 short · under 1%

**p−1 log-N:** **3/8** far moduli · pin D1D38A **not edited**

Spectral start is the Laplacian quadratic form of MaxCut (\(x^T L x = 4\cdot\mathrm{cut}\)). 3-flip is a φ-walk of triples. p−1 is modular exponentiation up to a bit-length smoothness bound.

## p−1 (log-N)

| p | q | B | Fold | Method | OK |
|--:|--:|--:|------|--------|:--:|
| 10007 | 1000003 | 816 | `None` | `pminus1_exhausted` | False |
| 10007 | 10000019 | 888 | `None` | `pminus1_exhausted` | False |
| 7919 | 104729 | 720 | `None` | `pminus1_exhausted` | False |
| 65537 | 100003 | 792 | `None` | `pminus1_exhausted` | False |
| 100003 | 1000003 | 888 | `None` | `pminus1_exhausted` | False |
| 31627 | 1000033 | 840 | `[31627, 1000033]` | `pminus1_logN` | True |
| 104729 | 1000003 | 888 | `[104729, 1000003]` | `pminus1_logN` | True |
| 1000003 | 1000033 | 960 | `[1000003, 1000033]` | `pminus1_logN` | True |

RSA-2048 p−1 bound B=`49152` (not run). Typical RSA primes have a large factor of p−1 above that bound.

```powershell
python -m fsot_quantum.heights_next
```
