# Heights 6 — ECM at 46-bit far p±1-unsmooth

**ECM:** **8/8** · log-N **8/8**

heights5 was 41-bit. This board is ~46-bit (`1.2e6 × 4e7`). Both p−1 and p+1 unsmooth at B2; kN-Fermat misses. Same B / B2, seed-locked curves. No new coefficient.

G17 remains `3034` vs 3047 (**13 edges**).

| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |
|--:|--:|-----:|-----|-----|----|-----|------|:--:|
| 1200917 | 40000003 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1200917 | 40000033 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1200917 | 40000283 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1200917 | 40000487 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1200917 | 40000517 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1202231 | 40000003 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1202231 | 40000033 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 1202231 | 40000283 | 46 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |

RSA-2048: B=`49152` still (not run). 46-bit is not 2048-bit.

```powershell
python -m fsot_quantum.heights6
```
