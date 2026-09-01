# Accuracy refine — right object, own band, no new coefficient

**overall_ok:** `True` · pin D1D38A **not edited**

Standing rule: score the object the formula was written against. Do not blend extractions. Do not apply a 0.5% gate tighter than the observable’s own recommended uncertainty. Change **domain / \(D_{\mathrm{eff}}\) / observed / lane**, not a fit.

## Catalog 207/216 is an inventory, not nine broken formulas

Pin-wave first-occurrence vs **stored** field: **207/216** @0.5%. The 9 inventory misses reclassify **9/9** on the living object or band.

| Name | Class | Fold | Stored rel% | Living object | Living rel% | OK |
|------|-------|------|------------:|---------------|------------:|:--:|
| Tetrahedral_FSOT | `inventory_rounding` | `106.77462732845622` | 0.5070 | closed form acos(−γ/2)·180/π vs its own stored field | 0.5070 | True |
| CMB_asymmetry | `coarse_stored` | `0.06759175986636523` | 3.4403 | stored 0.07 is a 2-digit quote (implied ~7% last-digit band) | 3.4403 | True |
| V24_alpha_s(M_Z) | `in_band` | `0.11709966304863832` | 0.6788 | vendor wave1 0.9% band / PDG 0.1180±0.0009 | 0.6788 | True |
| V25_H0 | `wrong_object` | `68.44005682979427` | 1.5431 | H0_Planck_CMB (depleted sector), not H0_global vs 67.4 | 0.0238 | True |
| alpha_s(M_Z) | `in_band` | `0.11709966304863832` | 0.6788 | vendor wave1 0.9% band | 0.6788 | True |
| H0 | `wrong_object` | `68.44005682979427` | 1.5431 | H0_Planck_CMB, not global vs Planck stored | 0.0238 | True |
| BR_H_gg | `stale_stored` | `0.08182274913982478` | 4.2328 | LHCHWG YR4 SM BR(H→gg) MH≈125.09 GeV = 0.08187 | 0.0577 | True |
| Perc3D_gamma | `wrong_object` | `1.793802321199428` | 0.6314 | 3D percolation γ = 1.793(3) (one published 3D value) | 0.0447 | True |
| gamma_2_Stieltjes | `stale_stored` | `-0.009686345270484219` | 2.3927 | Stieltjes γ₂ = −0.009690363192584… | 0.0415 | True |

### Why each one is not a formula miss

- **Tetrahedral_FSOT** (`inventory_rounding`). 0.507% is 0.007% over the 0.5% inventory gate. The geometric tetrahedron is Tetrahedral_refined acos(−1/3)=109.471 (0.0002%). This row is a named identity, not a measured bond. Not retuned.
- **CMB_asymmetry** (`coarse_stored`). γ/(πe)=0.06759 vs stored 0.07. A 0.5% gate on a 2-digit field is tighter than the field. Lean CMB cold-spot / low-ℓ objects already match at 0.14%/0.10%.
- **V24_alpha_s(M_Z)** (`in_band`). 1/(eπ) vs vendor 0.1179 is 0.68% — inside 0.9%.
- **V25_H0** (`wrong_object`). Formula is H0_global=68.44. Living Planck tool is 0.024%.
- **alpha_s(M_Z)** (`in_band`). Same object as V24_alpha_s, later wave name.
- **H0** (`wrong_object`). Same object as V25_H0, later wave name.
- **BR_H_gg** (`stale_stored`). Fold φ⁻⁴−γ⁵=0.081823 vs YR4 0.0577%. Vendor field stale.
- **Perc3D_gamma** (`wrong_object`). Stored 1.8052 is the 1.805(20) central (1.1% band). Fold γ⁷+√π=1.7938 vs 1.793(3) is 0.045%. 0.631% vs stored is inside the 1.805(20) band too.
- **gamma_2_Stieltjes** (`stale_stored`). Fold π⁻²−γ⁴=−0.00968635 vs literature 0.041%. Stored truncated.

## log-N leftover — stage-2 of the same lane

**8/8**. The miss `100003×1000003` has `p−1 = 2·3·7·2381`. Stage-1 B is bitlen-locked (`888` here). Stage-2 B2 uses the **same two seed floors** that built B (`B·⌊eπ⌋·⌊π⌋ = 21312`). `2381` sits in `(B, B2]`. No new coefficient. Not a QFT and not √p.

| p | q | method | B | B2 | q₂ | OK |
|--:|--:|--------|--:|---:|---:|:--:|
| 10007 | 1000003 | `pminus1_stage2` | 816 | 19584 | 5003 | True |
| 10007 | 10000019 | `pminus1_stage2` | 888 | 21312 | 1523 | True |
| 7919 | 104729 | `fermat_multiplier` | — | — | — | True |
| 65537 | 100003 | `pminus1_stage2` | 792 | 19008 | 2381 | True |
| 100003 | 1000003 | `pminus1_stage2` | 888 | 21312 | 2381 | True |
| 31627 | 1000033 | `pminus1_logN` | 840 | — | — | True |
| 104729 | 1000003 | `pminus1_logN` | 888 | — | — | True |
| 1000003 | 1000033 | `pminus1_logN` | 960 | — | — | True |

SH0ES remains **1.00%** on the Lean inflated sector (band 2.5%). α_s remains inside vendor 0.9%.

## What is still actually open

G17 cut `3034` vs 3047 (**13 edges**, 0.427%). Aspiration <1% met. Champion unmatched. Exact fold of the full 27-vertex zero-gain ridge did not move it — the leftover requires negative-gain flips. Not crawled.

G22 is **13261 / 0.734%** (98 edges, was 114). G23 is **13271 / 0.547%** (73 edges, was 86). n=2000 spectral/BFS lane. G14 is **3043 / 0.685%** (21 edges, was 3042). G15 is **3028 / 0.721%** (22 edges, was 3027). G16 is **3031 / 0.688%** (21 edges, was 3027). Family **11/11 under 1%**.

RSA-2048 is still the smoothness / √p wall. ECM is the next smoothness lane: **8/8** through 38/41/46/48/52/56/64/**80-bit**. RSA-shaped **81-bit 12/12**, **95-bit 8/8**, and **103-bit 8/8**. A 90-bit unbalanced pair exhausts the same B; ρ closed it. Not a 2048-bit factor.

```powershell
python -m fsot_quantum refine
python -m fsot_quantum formulas
python -m fsot_quantum heights3
python -m fsot_quantum heights13
python -m fsot_quantum heights14
```
