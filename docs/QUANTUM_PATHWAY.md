# Alternative quantum computing pathway (FSOT)

## What this is

An **FSOT-native** quantum *capability* — not a simulator of industry gate-model qubits on \(\mathbb{C}^{2^n}\).

Industry quantum:

- Complex amplitudes, Born rule, unitary matrices  
- Many free calibration parameters in hardware stacks  

FSOT quantum:

- Trinary fluid spins \(\{-1,0,+1\}\)  
- Collapse threshold \(\Theta=C_{\mathrm{eff}}P_{\mathrm{var}}\) from seeds only  
- Gates = FSOT trit ops + domain scalar routing  
- Bare-metal GPU kernels (CUDA) for pack / collapse / coupling  

## Why GPU bare metal

Same doctrine as FSOT-GPU and fsot-neuron-zig:

1. Semantics are trinary  
2. Binary buses may **carry** packed words (2 bits/trit)  
3. ALU / kernels implement trinary law, not “binary neural net theater”

Target hardware validated on sibling stack: **NVIDIA GeForce RTX 5070 (CC 12.0)**.

## Gate set

| Gate | Law |
|------|-----|
| X | `neg(t) = -t` |
| Z | `pair(t, phase_class(S_domain))` |
| H | poles → superposed; superposed → `sign(S)` |
| S | `sum_sat(t, phase_class)` |
| CX | control +1 flip; 0 super; −1 hold |
| CZ | control-gated Z |
| CCX | both controls +1 → flip |
| CONSENSUS / PAIR | FSOT machine ops |

Full table: `fsot_quantum/gates.py` → `GATE_TABLE`.

## Measurement

1. If continuous field present → `collapse_scalar` with \(\Theta\).  
2. If discrete superposed remains → resolve with `sign(S(domain))`.  
3. Eigenstates \(\pm 1\) are fixed under measure.

## Layers

```
vendor/fsot_compute.py     pin D1D38A authority
fsot_quantum/*             host engine + circuits
cuda/fsot_quantum.cu       bare-metal GPU kernels
formal/TrinaryQuantum.lean spin / pack spec
parity/                    vendor numeric twin
```

## Roadmap (no free params)

1. Expand multi-spin consensus entanglement panels  
2. Formal Lean obligations for gate identities (export spine)  
3. Larger CUDA step: full circuit interpreter on device  
4. Cross-domain residual panels under Quantum_Computing fold  
