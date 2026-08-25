# Heights 13 — RSA-shaped 48-bit × 48-bit (95-bit N)

**8/8** · classical-record direction on a consumer PC

Two similar-bit primes, not twins. p±1 and Fermat miss at our B. End-job ECM or Pollard ρ. This is the object cryptographers mean (balanced bits). Not RSA-100 / RSA-250 / RSA-2048.

See `docs/CLASSICAL_RECORDS.md`.

G17 remains `3034` vs 3047 (**13 edges**).

| p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |
|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage1` | `ecm_stage1` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |
| 48 | 48 | 95 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_stage2` | `ecm_stage2` | True |

RSA-2048: B=`49152` still (not run).

```powershell
python -m fsot_quantum.heights13
```
