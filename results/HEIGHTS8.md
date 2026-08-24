# Heights 8 — ECM at 52-bit far p±1-unsmooth

**ECM:** **8/8** · log-N **8/8**

heights7 was 48-bit. This board is ~52-bit (`1.2e7 × 2e8`). Same B / B2, seed-locked curves. No new coefficient.

G17 remains `3034` vs 3047 (**13 edges**). RSA-2048 still not run.

| p | q | bits | p−1 | p+1 | kN | ECM | logN | OK |
|--:|--:|-----:|-----|-----|----|-----|------|:--:|
| 12000253 | 200000083 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000253 | 200000117 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000253 | 200000161 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000253 | 200000209 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000281 | 200000083 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000281 | 200000117 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000467 | 200000083 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 12000643 | 200000083 | 52 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |

RSA-2048: B=`49152` still (not run). 52-bit is not 2048-bit.

```powershell
python -m fsot_quantum.heights8
```
