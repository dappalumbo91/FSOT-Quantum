# Heights 11 — ECM at 80-bit far p±1-unsmooth

**ECM:** **8/8** · log-N **8/8**

heights10 was 64-bit. This board is **80-bit** (`4e9 × 3e14`). Same B / B2, seed-locked curves. No new coefficient.

G17 remains `3034` vs 3047 (**13 edges**). RSA-2048 still not run.

| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |
|--:|--:|-----:|-----|-----|----|-----|------|:--:|
| 4000000019 | 300000000000089 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000019 | 300000000000097 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000019 | 300000000000179 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000019 | 300000000000187 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000063 | 300000000000089 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000063 | 300000000000097 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000133 | 300000000000089 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 4000000187 | 300000000000089 | 80 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |

RSA-2048: B=`49152` still (not run). 80-bit is not 2048-bit.

Next wall (same B / B2, not retuned): a 90-bit far pair `8000000081 × 100000000000000003` returns `ecm_exhausted` (58344 steps). The 8-digit-scale factor is no longer B-smooth in the elliptic group. Written, not crawled.

```powershell
python -m fsot_quantum.heights11
```
