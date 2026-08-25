# Heights 12 — RSA-shaped balanced 81-bit + 90-bit ρ

**12/12** · 90-bit unbalanced **4/4** · 81-bit balanced **8/8**

ECM smoothness is not the PC wall. The 90-bit ECM miss has a 33-bit factor; Pollard ρ (already on this path) hits in ~1e5 steps. The 81-bit board is two **41-bit** primes, far apart: p±1 and Fermat miss. End-job is ECM or ρ. Same seeds. No new coefficient.

See `docs/CONSUMER_VS_QPU.md`: innovative vs QPU, not vs GNFS.

G17 remains `3034` vs 3047 (**13 edges**).

| kind | p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |
|------|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|
| unbal_90 | 33 | 57 | 90 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| unbal_90 | 33 | 57 | 90 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| unbal_90 | 33 | 57 | 90 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| unbal_90 | 33 | 57 | 90 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| bal_81 | 41 | 41 | 81 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |

RSA-2048: B=`49152` still (not run).

```powershell
python -m fsot_quantum.heights12
```
