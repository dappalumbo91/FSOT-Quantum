# Heights 3 — log-N factor (p−1 + p+1 + kN Fermat)

**log-N:** **8/8** far moduli · p−1 7/8 · p+1 7/8 · kN-Fermat 3/8

G17 remains `3034` vs 3047 (**13 edges**, 0.427%). π³ breakout did not close it. Family is already 11/11 under 1%.

These three methods are **poly(log N)** once B and the Fermat cap are locked to bit length. They are not Pollard ρ (√p) and not a QFT.

| p | q | p−1 | p+1 | kN Fermat | logN | OK |
|--:|--:|-----|-----|-----------|------|:--:|
| 10007 | 1000003 | `pminus1_stage2` | `pplus1_logN` | `fermat_multiplier_exhausted` | `pminus1_stage2` | True |
| 10007 | 10000019 | `pminus1_stage2` | `pplus1_logN` | `fermat_multiplier_exhausted` | `pminus1_stage2` | True |
| 7919 | 104729 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier` | `fermat_multiplier` | True |
| 65537 | 100003 | `pminus1_stage2` | `pplus1_logN` | `fermat_multiplier` | `pminus1_stage2` | True |
| 100003 | 1000003 | `pminus1_stage2` | `pplus1_stage2` | `fermat_multiplier_exhausted` | `pminus1_stage2` | True |
| 31627 | 1000033 | `pminus1_logN` | `pplus1_stage2` | `fermat_multiplier_exhausted` | `pminus1_logN` | True |
| 104729 | 1000003 | `pminus1_logN` | `pplus1_logN` | `fermat_multiplier_exhausted` | `pminus1_logN` | True |
| 1000003 | 1000033 | `pminus1_logN` | `pplus1_stage2` | `fermat_multiplier` | `pminus1_logN` | True |

RSA-2048: B=`49152` still (not run). Stage-2 B2 uses the same seed floors as B. The old miss `100003×1000003` is `p−1 = 2·3·7·2381` — stage-2, not a new coefficient.

```powershell
python -m fsot_quantum.heights3
```
