# Genetics codon / 7-trit branching (this pin)

**overall_ok:** `True` · **15/15** · pin D1D38A **not edited** · genetics repo **not edited**

The codon map and 7-trit opcode live here as a copy of the FSOT-Genetics law (`genetics_law.py`). Each trit is a **Biology** fold. Word density is the product of independent \(|S|\) trit densities. Primary and secondary are two readouts — not averaged.

Biology \(D_{\mathrm{eff}}=12\), unobserved table \(S=0.444725\). Three-fold densities \(w_{+1}=0.1476\), \(w_{-1}=0.7021\), \(w_0=0.1503\).

## CGG → TGG (R → W)

C and T are both primary \(-1\). The mutation is the **secondary** first base \(0\to-1\) (superposed \(\to\) down). `dens(TGG)/dens(CGG) = w(-1)/w(0) = 4.670202`.

| Codon | AA | primary | secondary |
|-------|----|---------|-----------|
| CGG | R | `[-1, 1, 1]` | `[0, 0, 0]` |
| TGG | W | `[-1, 1, 1]` | `[-1, 0, 0]` |

Start ATG density (renormalized over 64) `0.000899`. Three stops together `0.002679`.

## Checks

| ID | Question | OK |
|----|----------|:--:|
| `codon_64` | Are there 64 DNA codons? | True |
| `opcode_20_unique` | Do 20 AA 7-trit words match the published genetics table? | True |
| `cgg_primary_secondary` | CGG primary/secondary = [−1,+1,+1] / [0,0,0]? | True |
| `tgg_primary_secondary` | TGG primary/secondary = [−1,+1,+1] / [−1,0,0]? | True |
| `cgg_tgg_is_secondary_collapse` | Is CGG→TGG a secondary 0→−1 on the first base (not a primary flip)? | True |
| `translate_cgg_tgg` | Does CGG→TGG translate R→W? | True |
| `cgg_tgg_density_ratio` | Is dens(TGG)/dens(CGG) = w(−1)/w(0) on Biology? | True |
| `no_average_C` | Primary C=−1 and secondary C=0 are not averaged? | True |
| `trit_not_atg_primary` | trit_not of ATG primary [+1,−1,+1] is [−1,+1,−1]? | True |
| `start_stop` | ATG is start M; TAA/TAG/TGA are the three stops? | True |
| `codon_measure_partition` | Do 64 codon |S|-word densities renormalize to 1? | True |
| `stop_vs_start_density` | Are stop and start codon densities computed (not fitted)? | True |
| `biology_unobserved_is_zero_fold` | Is living Biology table S the 0-trit (unobserved) fold? | True |
| `R_W_opcode_distinct` | Are R and W 7-trit words distinct with positive densities? | True |
| `pin_untouched` | Genetics repo not edited; pin D1D38A only? | True |

## What we did not do

- Did not edit [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics).
- Did not invent a codon table or a 7-trit fit.
- Did not average primary and secondary.
- Did not post a Born rule.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.genetics_branch
```
