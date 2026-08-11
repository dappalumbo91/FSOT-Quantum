# Architecture

```
                    FSOT-2.1-Lean (pin D1D38A)
                              |
              +---------------+---------------+
              |               |               |
         seeds/scalar    domains QM/QC    trinary Θ
              |               |               |
              +------- fsot_quantum (Python host) ----+
                              |
              +---------------+---------------+
              |                               |
        Circuit / Gates                  gpu_host.py
              |                               |
        TritRegister                    cuda/*.cu kernels
        measure / collapse              pack · collapse · CX · consensus
```

## Packages

| Path | Role |
|------|------|
| `fsot_quantum/seeds.py` | Layer 0/1/2 constants + pin helper |
| `fsot_quantum/scalar.py` | \(S=K(T_1+T_2+T_3)\) |
| `fsot_quantum/domains.py` | QM / QC interfaces |
| `fsot_quantum/trinary.py` | Spin algebra + pack |
| `fsot_quantum/qubit.py` | Trit register |
| `fsot_quantum/gates.py` | Gate set |
| `fsot_quantum/circuit.py` | Circuit runner |
| `fsot_quantum/measure.py` | Collapse / resolve |
| `fsot_quantum/verify.py` | Gates for CI / local |
| `cuda/fsot_quantum.cu` | Bare-metal CUDA |
| `vendor/fsot_compute.py` | Byte pin authority |

## Data flow (one step)

1. Encode classical bits or zeros → `TritRegister`  
2. Apply FSOT gates (domain-routed)  
3. Optional GPU pack / batch collapse  
4. Measure → eigen-spins in \(\{-1,+1\}\) (or rare residual 0 if \(S=0\))  
5. Ledger JSON under `results/`  
