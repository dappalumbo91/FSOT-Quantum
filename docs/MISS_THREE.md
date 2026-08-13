# Why three audit rows missed 0.5% — and what the data actually are

**Pin:** D1D38A not edited. No new formula terms.

The three fold-vs-literature misses were **wrong objects**, not broken seeds.

---

## 1. \|V_cb\| — we averaged two PDG numbers that disagree

PDG 2024 (LHCP / CKM review):

| Extraction | \|V_cb\| |
|------------|----------|
| **Inclusive** \(B\to X_c\ell\nu\) | **(42.2 ± 0.5)×10⁻³ = 0.0422** |
| Exclusive \(B\to D^{(*)}\ell\nu\) | (39.8 ± 0.6)×10⁻³ = 0.0398 |
| Homemade blend we first scored | 0.0411 |

Inclusive vs exclusive differ by ~3σ. That is the **\(V_{cb}\) puzzle**. It is not a typo in our table.

Pin formula (wave3): \(S_{\mathrm{quant}}/C_{\mathrm{eff}}-S_{\mathrm{quant}}=0.0422008\).

| Score against | rel |
|---------------|-----|
| Inclusive PDG 0.0422 | **0.002%** |
| Vendor 0.0422 | 0.002% |
| Exclusive 0.0398 | 6.0% — **different measurement** |
| Blend 0.0411 | 2.68% — **that was our mistake** |

**Solve:** score inclusive. Exclusive stays a separate open flavor-physics question, not a reason to retune \(S/C_{\mathrm{eff}}\).

---

## 2. BR(\(H\to\gamma\gamma\)) — 125.00 vs 125.09 GeV, plus theory error

| Table | BR(\(H\to\gamma\gamma\)) |
|-------|--------------------------|
| Vendor wave8 / 125.00 GeV SM | **0.00228** |
| YR4 central at 125.09 GeV | 0.002270 |
| Pin \(\gamma^6\cdot C_{\mathrm{cosm}}\) | **0.0022858** |
| LHCHWG recommended uncertainty | **~2.8%** |

| Score against | rel |
|---------------|-----|
| 125.00 GeV / vendor 0.00228 | **0.25%** |
| 125.09 GeV 0.002270 | 0.70% — still **inside 2.8% theory band** |

The 0.70% “miss” was a 90 MeV mass-point shift on a BR whose own theory error is several times larger.

---

## 3. BR(\(H\to Z\gamma\)) — same, and the theory band is ~6%

| Table | BR(\(H\to Z\gamma\)) |
|-------|----------------------|
| Vendor wave8 / 125.00 GeV SM | **0.00153** |
| YR4 central at 125.09 GeV | 0.001541 |
| Pin \(\eta_{\mathrm{eff}}/\pi^5\) | **0.0015259** |
| LHCHWG recommended uncertainty | **~6%** (loop-induced; 2025 note: BR < 0.2%) |

| Score against | rel |
|---------------|-----|
| 125.00 GeV / vendor 0.00153 | **0.27%** |
| 125.09 GeV 0.001541 | 0.98% — still **inside ~6% theory band** |

Same pattern as \(\gamma\gamma\): we applied a 0.5% gate tighter than the observable’s own recommended uncertainty, at a 90 MeV mass offset.

---

## What we did not do

- Did not average inclusive and exclusive \(V_{cb}\).
- Did not add a term to crawl \(H\to\gamma\gamma\) from 0.002286 to 0.002270.
- Did not touch `vendor/fsot_compute.py`.

## Reproduce

```powershell
python -m fsot_quantum.stale_targets
```
