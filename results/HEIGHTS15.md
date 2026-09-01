# Heights 15 — RSA-shaped 56-bit × 56-bit (~111-bit N)

**8/8** · classical-record direction on a consumer PC

Two similar-bit primes, not twins. p±1 and Fermat miss at our B. End-job ECM or Pollard ρ. This is the object cryptographers mean (balanced bits). Not RSA-100 / RSA-250 / RSA-2048.

See `docs/CLASSICAL_RECORDS.md`.

G17 remains `3034` vs 3047 (**13 edges**).

| p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |
|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|
| 56 | 56 | 111 | `pminus1_stage2` | `pplus1_stage2` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pminus1_stage2` | True |
| 56 | 56 | 111 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 56 | 56 | 111 | `pminus1_stage2` | `pplus1_stage2` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pminus1_stage2` | True |
| 56 | 56 | 111 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 56 | 56 | 111 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 56 | 56 | 111 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 56 | 56 | 111 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 56 | 56 | 112 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |

RSA-2048: B=`49152` still (not run).

```powershell
python -m fsot_quantum.heights15
```
