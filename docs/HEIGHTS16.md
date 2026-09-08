# Heights 16 — RSA-shaped 64-bit × 64-bit (~127-bit N)

**0/8** · classical-record direction on a consumer PC

Two similar-bit primes, not twins. p±1 and Fermat miss at our B. ECM at the **locked** B is the score. Pollard ρ on 64-bit \(p\) is \(\sim 2^{32}\) steps — a rho run on the first pair was still open after 35 minutes and was stopped. Not RSA-100 / RSA-2048.

See `docs/CLASSICAL_RECORDS.md`.

G17 remains `3034` vs 3047 (**13 edges**).

| p bits | q bits | N bits | p−1 | p+1 | kN | ECM | end | OK |
|-------:|-------:|-------:|-----|-----|----|-----|-----|:--:|
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 127 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 128 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 128 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |
| 64 | 64 | 128 | `pminus1_exhausted` | `pplus1_exhausted` | `fermat_multiplier_exhausted` | `ecm_exhausted` | `ecm_exhausted` | False |

RSA-2048: B=`49152` still (not run).

```powershell
python -m fsot_quantum.heights16
```
