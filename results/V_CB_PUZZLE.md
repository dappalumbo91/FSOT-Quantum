# The \(|V_{cb}|\) puzzle — same algebra, different domain

**overall_ok:** `True` · pin D1D38A **not edited**

Inclusive and exclusive \(|V_{cb}|\) disagree by ~3σ in the data. That is the **\(V_{cb}\) puzzle**. It is not a reason to retune \(S_{\mathrm{QM}}/C_{\mathrm{eff}}-S_{\mathrm{QM}}\).

Inclusive is an OPE / moment extraction (\(B\to X_c\ell\nu\)). Exclusive is a single-channel + lattice form-factor extraction (\(B\to D^{(*)}\ell\nu\)). Those are different **looks**. FSOT changes **domain / \(D_{\mathrm{eff}}\)**, not a coefficient.

Same pin form \(S\cdot(1/C_{\mathrm{eff}}-1)\):

| Extraction | Domain | \(D_{\mathrm{eff}}\) | Fold | PDG 2024 | rel | σ | OK |
|------------|--------|----------------------:|------|----------|----:|--:|:--:|
| inclusive | Quantum_Mechanics | 6 | `0.04220081` | `0.0422` ± 0.0005 | 0.002% | 0.00 | True |
| exclusive | High_Energy_Physics | 7 | `0.03914267` | `0.0398` ± 0.0006 | 1.652% | 1.10 | True |

Exclusive PDG uncertainty is ±0.0006 (**1.51%**). A 0.5% gate is tighter than the exclusive measurement. HEP sits **1.1σ** from exclusive 0.0398 — inside 2σ, not a 0.5% claim.

## What we did not do

- Did not average 0.0422 and 0.0398.
- Did not add a term to crawl 0.04220 down to 0.0398.
- Did not score **Astronomy** (fold 0.03968, 0.30% from exclusive). That domain is not exclusive \(B\) decay. Number-matching is theater.
- Did not touch `vendor/fsot_compute.py`.

Neighbor checks (not scored): Particle_Physics \(D=5\) is 0.53% from inclusive. Nuclear_Physics is 2.24% from exclusive.

```powershell
python -m fsot_quantum.vcb_puzzle
```
