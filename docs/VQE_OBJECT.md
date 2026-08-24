# VQE objects — H2 energy is not one number

**overall_ok:** `True` on pin objects + amplitude estimation. Kolos residual is written, not retuned. STO-3G not scored. LiH FCI not invented.

NISQ VQE is hired for H2/LiH *electronic energy in a tiny basis*. That is not the pin H−H bond energy and not Kolos–Wolniewicz. Same lesson as \(V_{cb}\) and \(H_0\): score the object.

| Object | Formula | Fold | Published | rel% | OK |
|--------|---------|------|-----------|-----:|:--:|
| H−H dissociation (kJ/mol) — pin chemistry | `e⁸/φ⁴` | `434.91590900168626` | `436.0` | 0.2486 | True |
| H−H bond length (Å) — geometry VQE scans | `sin(1) − π⁻²` | `0.7401498011655587` | `0.74` | 0.0202 | True |
| H2 total energy (Ha) from 2 E(H) − De vs Kolos–Wolniewicz | `2(−1/2) − (e⁸/φ⁴)/Eh` | `-1.1656507212805611` | `-1.174475` | 0.7513 | False |
| STO-3G FCI H2 (NISQ VQE demo) — not scored | `—` | `-1.1656507212805611` | `-1.137` | 2.5199 | True |
| LiH electronic FCI — no pin formula | `—` | — | — | — | True |
| Amplitude estimation a = |S|/2^n (k=5, n=5) | `k / 2^n` | `0.15625` | `0.15625` | 0.0000 | True |

### Notes

- **BE_H-H.** Textbook De. Already in chemistry 68/68.
- **BL_H-H.** STO-3G VQE plots vs R; eq ~0.74 Å.
- **E_H2_kolos.** Derived from the pin De, not a new coefficient. 0.0088 Ha vs chemical accuracy 0.0016 Ha. Not crawled. Kolos is the spectroscopic electronic object.
- **E_H2_sto3g.** Wrong object if scored as Kolos or as pin De. Tiny-basis FCI is what Kandala-class VQE matches. We refuse to blend it with (1) or (3).
- **LiH_FCI.** No Li−H seed formula. Not invented. Not scored.
- **amp_est.** Quantum counting end-job. Exact on the marked set.

G17 remains 3034 / 13 edges. Champion unmatched. Not crawled.

```powershell
python -m fsot_quantum.vqe_object
python -m fsot_quantum vqe
```
