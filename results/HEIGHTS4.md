# Heights 4 — ECM on p±1-unsmooth far moduli

**ECM:** **8/8** · log-N (p±1 + kN + ECM) **8/8**

G17 remains `3034` vs 3047 (**13 edges**, 0.427%). Exact fold of the full 27-vertex zero-gain ridge did not move it. The leftover 13 edges require negative-gain flips. Not crawled.

These moduli are the RSA-shaped leftover after stage-2: both p−1 and p+1 unsmooth at B2, primes far apart so kN-Fermat misses. ECM uses the **same** B / B2 and seed-locked curves. No new coefficient. Not a QFT.

| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |
|--:|--:|-----:|-----|-----|----|-----|------|:--:|
| 140683 | 1000289 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 140683 | 1000291 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 140683 | 1000423 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 142123 | 1000289 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 143357 | 1000289 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 144427 | 1000289 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 146347 | 1000289 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 146837 | 1000289 | 38 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |

RSA-2048: B=`49152` still (not run). ECM is the next smoothness lane, not a 2048-bit factor.

```powershell
python -m fsot_quantum.heights4
```
