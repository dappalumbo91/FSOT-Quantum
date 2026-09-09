# Heights 16 — RSA-shaped 64-bit × 64-bit (~127-bit N)

**8/8** · classical-record direction on a consumer PC

Two similar-bit primes, not twins. p±1, Fermat, and ECM miss at the **locked** B. End-job is CFRAC (same B, B2 large-prime pairing) or Brent ρ with batched GCD (same three seeds). Not RSA-100 / RSA-2048.

See `docs/CLASSICAL_RECORDS.md`.

G17 remains `3034` vs 3047 (**13 edges**).

| p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |
|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `cfrac_smooth` | True |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `cfrac_smooth` | True |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `cfrac_smooth` | True |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 64 | 64 | 128 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `pollard_rho_seed` | True |
| 64 | 64 | 128 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `cfrac_smooth` | True |
| 64 | 64 | 128 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `cfrac_smooth` | True |

RSA-2048: B=`49152` still (not run).

```powershell
python -m fsot_quantum.heights16
```
