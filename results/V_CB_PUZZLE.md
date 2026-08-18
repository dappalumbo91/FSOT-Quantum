# The \(|V_{cb}|\) puzzle — same algebra, different domain

**overall_ok:** `True` · pin D1D38A **not edited**

Inclusive and exclusive \(|V_{cb}|\) disagree by ~3σ in the data. That is the **\(V_{cb}\) puzzle**. It is not a reason to retune \(S_{\mathrm{QM}}/C_{\mathrm{eff}}-S_{\mathrm{QM}}\).

Inclusive is an OPE / moment extraction (\(B\to X_c\ell\nu\)). Exclusive \(B\to D\ell\nu\) is a single-channel + lattice form-factor extraction (Belle II 2025). Combined exclusive 0.0398 blends D and D* and is **not** the HEP object. FSOT changes **domain / \(D_{\mathrm{eff}}\)**, not a coefficient.

Same pin form \(S\cdot(1/C_{\mathrm{eff}}-1)\):

| Extraction | Domain | \(D_{\mathrm{eff}}\) | Fold | Published | rel | σ | OK |
|------------|--------|----------------------:|------|-----------|----:|--:|:--:|
| inclusive | Quantum_Mechanics | 6 | `0.04220081` | `0.0422` ± 0.0005 | 0.002% | 0.00 | True |
| exclusive_BD | High_Energy_Physics | 7 | `0.03914267` | `0.0392` ± 0.00088 | 0.146% | 0.07 | True |

Belle II \(B\to D\ell\nu\) is \(0.0392\pm 0.00088\). HEP is **0.146%** from that central (0.07σ). Combined exclusive 0.0398 is a D+D* blend (HEP vs blend 1.65%, 1.10σ) — not scored as the object.

## What we did not do

- Did not average 0.0422 and 0.0398.
- Did not add a term to crawl 0.04220 down to 0.0398.
- Did not score **Astronomy**. That domain is not exclusive \(B\) decay.
- Did not touch `vendor/fsot_compute.py`.

Neighbor checks (not scored): Particle_Physics \(D=5\) is 0.53% from inclusive.

```powershell
python -m fsot_quantum.vcb_puzzle
```
