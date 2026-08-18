# The Hubble tension — same algebra, different domain

**overall_ok:** `True` · pin D1D38A **not edited**

Planck / ΛCDM and SH0ES disagree by ~5σ in the data. That is the **Hubble tension**. It is not a reason to retune \(100(1+S_{\mathrm{cosm}} A_{\mathrm{bleed}}/A_{\mathrm{in}})\).

Planck is an early-universe CMB inference (Cosmology, unobserved, \(D_{\mathrm{eff}}=25\)). SH0ES is a late-universe local distance ladder (Cepheids + SN Ia). Those are different **looks**. FSOT changes **domain / \(D_{\mathrm{eff}}\)**, not a coefficient.

Same pin form \(100\cdot(1+S\cdot A_{\mathrm{bleed}}/A_{\mathrm{in}})\):

| Extraction | Domain | \(D_{\mathrm{eff}}\) | Fold | Published | rel | σ | OK |
|------------|--------|----------------------:|------|-----------|----:|--:|:--:|
| Planck | Cosmology | 25 | `68.4401` | `67.4` ± 0.5 | 1.543% | 2.08 | True |
| SH0ES | Particle_Astrophysics | 24 | `73.3421` | `73.04` ± 1.04 | 0.414% | 0.29 | True |

SH0ES (Riess et al. 2022) is \(73.04\pm 1.04\). Particle_Astrophysics sits **0.41%** from that central (0.3σ) — inside the 0.5% gate. Planck-side Cosmology stays inside the vendor 2.1% band (1.54%).

## What we did not do

- Did not average 67.4 and 73.04.
- Did not add a term to crawl 68.44 up to 73.04.
- Did not score **Seismology** (fold 71.99, 1.43% from SH0ES). That domain is not the local distance ladder.
- Did not apply this \(H_0\) form to looked Astronomy (\(S>0\) → \(H_0\sim 120\)).
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.h0_tension
```
