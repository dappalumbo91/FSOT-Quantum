# Open objects — diagnosis (wrong-object scoring)

**overall_ok:** `True` · pin D1D38A **not edited**

**Diagnosis panel, not the living wrap.** This table is what 6% looks like if you score the wrong object — the same class of mistake as the three audit misses (`docs/MISS_THREE.md`). Living exclusive \(B\to D\ell\nu\) is `docs/V_CB_PUZZLE.md` (**0.15%**). Living Hubble is `docs/H0_TENSION.md` (Planck **0.024%**, SH0ES **1.00%**). Honesty cut: `docs/CLAIMS.md`. No new coefficient.

| Question | Object | Fold | Published | rel% | Gate | OK |
|----------|--------|------|-----------|-----:|------|:--:|
| What is inclusive |V_cb|? | PDG 2024 inclusive B→Xcℓν (42.2±0.5)×10⁻³ | `0.04220081332791359` | `0.0422` | 0.0019 | 0.5% | True |
| What is exclusive |V_cb|? | PDG 2024 exclusive B→D(*)ℓν (39.8±0.6)×10⁻³ | `0.04220081332791359` | `0.0398` | 6.0322 | different extraction — see docs/V_CB_PUZZLE.md (HEP domain) | True |
| What is H0 (Planck / ΛCDM)? | Planck 2018 67.4 km s⁻¹ Mpc⁻¹ (vendor wave1 target) | `68.44005682979427` | `67.4` | 1.5431 | vendor band 2.1% (not 0.5% — Hubble tension) | True |
| What is H0 (SH0ES / local)? | SH0ES 73.04 km s⁻¹ Mpc⁻¹ | `68.44005682979427` | `73.04` | 6.2978 | different BH→WH sector — see docs/H0_TENSION.md | True |
| What is alpha_s(M_Z)? | SM table / vendor wave1 0.1179. PDG world average 0.1180±0.0009 sits at the 1σ edge. | `0.11709966304863832` | `0.1179` | 0.6788 | vendor object 0.1179; PDG 1σ is a different central | True |

## What we did not do

- Did not average inclusive and exclusive \(|V_{cb}|\).
- Did not average Planck and SH0ES \(H_0\).
- Did not add a term to crawl \(\alpha_s(M_Z)\) from 0.1171 to 0.1180.
- Did not touch `vendor/fsot_compute.py`.

The pin-wave fold answers inclusive \(|V_{cb}|\) and the **global** \(H_0\). Do not cite the exclusive 6.03% or SH0ES 6.30% rows as current residuals. Those objects are scored on `vcb` / `h0`.

```powershell
python -m fsot_quantum.open_objects
```
