# ORF climb — start-to-stop as a product of codon folds

**overall_ok:** `True` · **11/11** · pin D1D38A **not edited** · genetics repo **not edited**

An in-frame ORF is `ATG` + sense codons + stop. Density is the independent product of Biology \(|S|\) codon densities. A missense changes one codon. A frameshift is a different object.

| ORF | Peptide | Density |
|-----|---------|--------:|
| `ATG CGG TAA` | MR* | `2.895019e-12` |
| `ATG TGG TAA` | MW* | `1.352032e-11` |
| `ATG TAA` | M* | `5.571857e-08` |
| MQIFVK* (lawful CDS) | MQIFVK* | `2.110028e-25` |

Missense MR*→MW* (CGG→TGG) ratio **4.670202** = codon ratio (flanks cancel). 61 sense `ATG-XXX-TAA` mini-ORFs.

## Checks

| ID | Question | OK |
|----|----------|:--:|
| `orf_shape` | Are ATG-CGG-TAA / ATG-TGG-TAA / ATG-TAA / MQIFVK* in-frame ORFs? | True |
| `peptides` | Do those ORFs translate MR / MW / M / MQIFVK? | True |
| `orf_product_law` | Is ORF density the product of codon densities? | True |
| `missense_ratio_cancels_flanks` | Does dens(ATG-TGG-TAA)/dens(ATG-CGG-TAA) = dens(TGG)/dens(CGG)? | True |
| `frameshift_rejected` | Is a length-not-mod-3 string rejected (different object)? | True |
| `internal_stop_not_orf` | Is ATG-TAA-CGG-TAA rejected as an ORF (internal stop)? | True |
| `mini_orf_61_sense` | Are there 61 in-frame ATG-XXX-TAA sense mini-ORFs? | True |
| `atg_taa_is_met` | Is ATG-TAA an ORF that translates Met? | True |
| `mqifvk_seven_codons` | Is MQIFVK* seven codon folds (6 AA + stop)? | True |
| `mqifvk_q_to_r` | Does Q→R in MQIFVK* change density by dens(CGG)/dens(CAG) only? | True |
| `pin_untouched` | Genetics repo not edited; pin D1D38A only? | True |

## What we did not do

- Did not edit the genetics repository.
- Did not invent a coefficient for an ORF.
- Did not call MQIFVK* a sequenced genome; it is one lawful CDS for that peptide.
- Did not score a frameshift as the same object.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.orf_branch
```
