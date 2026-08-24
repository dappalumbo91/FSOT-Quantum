# Heights 5 — ECM at 41-bit far p±1-unsmooth

**ECM:** **8/8** · log-N **8/8**

heights4 was 38-bit. This board is ~41-bit (`400k × 4e6`). Both p−1 and p+1 unsmooth at B2; kN-Fermat misses. Same B / B2, seed-locked curves. No new coefficient.

G17 remains `3034` vs 3047 (**13 edges**). Zero-ridge windows and blob-exchange did not move the 13. Negative-gain leftover, not crawled.

| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |
|--:|--:|-----:|-----|-----|----|-----|------|:--:|
| 400277 | 4000043 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400277 | 4000063 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400277 | 4000093 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400277 | 4000357 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400277 | 4000573 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400853 | 4000043 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400853 | 4000063 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 400853 | 4000093 | 41 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |

RSA-2048: B=`49152` still (not run).

```powershell
python -m fsot_quantum.heights5
```
