# Open objects — different measurements, not pin misses

**overall_ok:** `True` · pin D1D38A **not edited**

These three were left open on the wrap on purpose. They are **different extractions**, the same class of mistake as the three audit misses (`docs/MISS_THREE.md`). No new coefficient.

| Question | Object | Fold | Published | rel% | Gate | OK |
|----------|--------|------|-----------|-----:|------|:--:|
| What is inclusive |V_cb|? | PDG 2024 inclusive B→Xcℓν (42.2±0.5)×10⁻³ | `0.04220081332791359` | `0.0422` | 0.0019 | 0.5% | True |
| What is exclusive |V_cb|? | PDG 2024 exclusive B→D(*)ℓν (39.8±0.6)×10⁻³ | `0.04220081332791359` | `0.0398` | 6.0322 | different extraction — not a 0.5% fail | True |
| What is H0 (Planck / ΛCDM)? | Planck 2018 67.4 km s⁻¹ Mpc⁻¹ (vendor wave1 target) | `68.44005682979427` | `67.4` | 1.5431 | vendor band 2.1% (not 0.5% — Hubble tension) | True |
| What is H0 (SH0ES / local)? | SH0ES 73.04 km s⁻¹ Mpc⁻¹ | `68.44005682979427` | `73.04` | 6.2978 | different extraction — not a 0.5% fail | True |
| What is alpha_s(M_Z)? | SM table / vendor wave1 0.1179. PDG world average 0.1180±0.0009 sits at the 1σ edge. | `0.11709966304863832` | `0.1179` | 0.6788 | vendor object 0.1179; PDG 1σ is a different central | True |

## What we did not do

- Did not average inclusive and exclusive \(|V_{cb}|\).
- Did not average Planck and SH0ES \(H_0\).
- Did not add a term to crawl \(\alpha_s(M_Z)\) from 0.1171 to 0.1180.
- Did not touch `vendor/fsot_compute.py`.

The fold answers inclusive \(|V_{cb}|\) and Planck-side \(H_0\). Exclusive \(V_{cb}\) and SH0ES stay separate flavor / cosmology questions.

```powershell
python -m fsot_quantum.open_objects
```
