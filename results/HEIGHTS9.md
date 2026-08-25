# Heights 9 — ECM at 56-bit far p±1-unsmooth

**ECM:** **8/8** · log-N **8/8**

heights8 was 52-bit. This board is ~56-bit (`4e7 × 1.5e9`). Same B / B2, seed-locked curves. No new coefficient.

G17 remains `3034` vs 3047 (**13 edges**). RSA-2048 still not run.

| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |
|--:|--:|-----:|-----|-----|----|-----|------|:--:|
| 40000003 | 1500000079 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 40000003 | 1500000113 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 40000003 | 1500000167 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 40000003 | 1500000233 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 40000033 | 1500000079 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 40000033 | 1500000113 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 40000283 | 1500000079 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 40000487 | 1500000079 | 56 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |

RSA-2048: B=`49152` still (not run). 56-bit is not 2048-bit.

```powershell
python -m fsot_quantum.heights9
```
