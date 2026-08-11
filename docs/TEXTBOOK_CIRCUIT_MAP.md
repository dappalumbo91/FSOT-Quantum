# Textbook quantum circuits → FSOT gates

| Industry | Job | FSOT gates |
|----------|-----|------------|
| X (NOT) | bit flip | `X 0` |
| H (Hadamard) | create superposition | `H 0` |
| Z | phase mark | `Z 0` |
| CNOT | entangling two-qubit | `CX 0 1` |
| Bell |Φ+⟩ prep | maximally entangled pair | `H 0 ; CX 0 1 ; MEASURE 0 ; MEASURE 1` |
| GHZ-3 prep | 3-party correlation | `H 0 ; CX 0 1 ; CX 1 2 ; MEASURE 0 ; MEASURE 1 ; MEASURE 2` |
| SWAP (via 3 CNOT) | exchange wires | `CX 0 1 ; CX 1 0 ; CX 0 1` |
| Toffoli (CCNOT) | classical reversible AND control | `CCX 0 1 2` |
| Deutsch–Jozsa skeleton | constant vs balanced oracle class | `H 0 ; H 1 ; H 2 ; CX 0 2 ; H 0 ; H 1 ; MEASURE 0 ; MEASURE 1` |
| Bernstein–Vazirani skeleton | learn secret bitstring | `H 0 ; H 1 ; H 2 ; H 3 ; CX 0 3 ; CX 2 3 ; H 0 ; H 1 ; H 2 ; MEASURE 0 ; MEASURE 1 ; MEASURE 2` |
| Grover iterate skeleton | amplify marked state | `H 0 ; H 1 ; H 2 ; Z 0 ; Z 1 ; Z 2 ; H 0 ; H 1 ; H 2` |
| Phase kickback lite | eigenphase onto control | `H 0 ; CZ 0 1 ; H 0 ; MEASURE 0` |
| QFT role (FSOT-GPU) | phase ladder / Fourier-like structure | `[device] coherence_norm → apply_phase_rotation → consensus_aggregate` |

**Run pass:** 13/13

Authority: `fsot_quantum/gates.py` + `fsot_lib` collapse/consensus.
