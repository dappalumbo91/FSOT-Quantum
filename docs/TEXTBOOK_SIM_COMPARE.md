# Textbook quantum simulator vs FSOT-QC (job-level)

FSOT trinary ≠ Hilbert amplitudes. Comparison is job-level, not state fidelity.

**overall_ok:** `True` (5/5)

| Job | Agreement | Note |
|-----|-----------|------|
| X / NOT on computational basis | True | Textbook |0>→|1>; FSOT +1→−1 polarity flip. |
| Bell Φ+ preparation / correlation | True | Textbook: 50/50 on 00&11. FSOT: deterministic agree after measure. |
| GHZ-3 correlation | True | Both establish 3-party correlated structure under their ontologies. |
| Deutsch–Jozsa constant-0 classification | True | Same job label; different query model (FSOT full scan n≤16). |
| Bernstein–Vazirani secret recovery s=101 | True | Both recover s exactly on parity oracle family. |

## Methods

- **Textbook:** pure-Python statevector, H/X/CX only, n≤3.
- **FSOT:** `fsot_lib` collapse/pack + `fsot_quantum` gates/circuits.
- **Not claimed:** amplitude fidelity, universal unitary simulation.
