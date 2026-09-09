# Heights 17 — RSA-shaped 60-bit × 60-bit (~119-bit N)

**8/8** · between 56-bit 8/8 and the 64-bit ρ wall

Two similar-bit primes, not twins. p±1 and Fermat miss at our B. End-job ECM or Pollard ρ. Not RSA-100 / RSA-2048.

See `docs/CLASSICAL_RECORDS.md`.

G17 remains `3034` vs 3047 (**13 edges**).

| p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |
|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 60 | 60 | 119 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |

RSA-2048: B=`49152` still (not run). 64-bit ECM is 0/8 (`HEIGHTS16.md`).

```powershell
python -m fsot_quantum.heights17
```
