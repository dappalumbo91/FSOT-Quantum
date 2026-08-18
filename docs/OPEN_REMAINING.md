# The leftovers — what is still open, and what was a wrong object

**overall_ok:** `True` · pin D1D38A **not edited** · G17 champion unmatched (13 edges, under 1%)

## 1. Dark energy — CMB vs BAO (this was the hidden split)

Lean `dark_energy_dual_readout_lib.py`: CMB lane and BAO lane, Catalan/π bleed. Vendor `w0` / `Dark_energy_wa` are the **CMB** lane. DESI DR2 is the **BAO** lane. Same lesson as \(V_{cb}\) and \(H_0\).

| Lane | w0 | wa |
|------|----|----|
| CMB | `-1.0299812921372637` (`−P_new·π/G`) | `-0.8081097715810811` (`−γ·e·φ/π`) |
| BAO | `-0.7296790154668923` vs DESI -0.727 (**0.369%**, 0.09σ) | `-1.020855644982926` vs DESI -1.018 (**0.281%**, 0.01σ) |

## 2. α_s(M_Z) — 0.68% is not a formula miss

`1/(eπ)` = `0.11709966304863834`. Vendor table 0.1179 (wave1 band **0.9%**). PDG world average 0.1180±0.0009 (**0.76%**). Fold vs vendor **0.679%** (inside 0.9%). A 0.5% gate is tighter than both the vendor band and the PDG 1σ. Lean treats `1/(eπ)` as the definition (cache match 1e−8). Not crawled.

## 3. Exclusive |V_cb| — score B→D, not the D+D* blend

Inclusive: QM `0.042201` vs 0.0422. Exclusive B→Dℓν (Belle II 2025): HEP `0.039143` vs **0.0392** (**0.146%**). Combined exclusive 0.0398 still blends D and D* — that was the 1.1σ leftover. See `docs/V_CB_PUZZLE.md`.

## 4. Gset G17 — aspiration met, champion unmatched

Cut 3034 vs champion 3047 (**0.427%**, 13 edges). Family **11/11 under 1%**. Planar G14 is 22 edges / 0.72%. Not a stale target and not a new coefficient. Champion still unmatched — written, not hidden.

## Lean anomalies (same pin, already solved there)

From `_ref/FSOT-2.1-Lean/data/cosmology_anomalies_benchmark.json`:

| Name | Mechanism | Fold | Measured | rel% |
|------|-----------|------|----------|-----:|
| S8_tension_Planck_vs_DES_Y3 | `wh_lensing_decay` | `0.05788678` | `0.058` | 0.1952 |
| S8_DES_Y3 | `local_lensing_depleted` | `0.77611322` | `0.776` | 0.0146 |
| Li7_over_H_observed | `skeleton_bbn` | `1.6000112966810868e-10` | `1.6e-10` | 0.0007 |
| CMB_cold_spot_significance | `wh_suction_void` | `5.00700629` | `5.0` | 0.1401 |
| CMB_low_ell_power_deficit | `wh_orifice_anisotropy` | `0.0999038` | `0.1` | 0.0962 |
| JWST_early_massive_galaxy_z | `recompactification_fast_track` | `14.0121683` | `14.0` | 0.0869 |
| FRB_DM_excess_vs_IGM | `bh_wh_tunnel_scatter` | `200.08522203` | `200.0` | 0.0426 |

```powershell
python -m fsot_quantum.open_remaining
```
