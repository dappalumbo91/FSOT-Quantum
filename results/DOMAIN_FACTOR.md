# Domain-fold factor — 35 pin D_eff on the RSA-100 miss

**miss** · pin D1D38A **not edited** · B **not raised** · factors **not looked up**

Same move as \(V_{cb}\) / \(H_0\): change **domain / \(D_{\mathrm{eff}}\)**, not a coefficient. Fermat \(k\) and ECM \(a\) are the 35 pin \(D_{\mathrm{eff}}\) values (and pairwise products). Locked B = `7920`, B2 = `190080`. 60-bit smoke split via `fermat_multiplier`.

RSA-100 is an artificial challenge modulus, not a pin observable. \(S(\mathrm{QC})\) does not encode its factors. If this lane misses, that is the smoothness / Fermat-gap wall, not a reason to edit the pin.

| rsa100 | `domain_factor_exhausted` | ok=False | fermat_k=185 | ecm_curves=27 | wall 715 s |

```powershell
python -m fsot_quantum.fold_domain_factor
```
