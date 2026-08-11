# Architecture

```
                 FSOT-2.1-Lean pin D1D38A
                            |
              seeds · scalar · domains QM/QC
                            |
                 fsot_quantum (owned ops)
                    trinary · gates · circuit · measure
                            |
              +-------------+-------------+
              |                           |
     pure Python host              device.py adapter
     (always works)                torch cuda if present
                                   (buffers + speed only)
```

**Not in the critical path:** custom `nvcc` / `.cu` product surface.

## Packages

| Path | Role |
|------|------|
| `fsot_quantum/seeds.py` | Layer 0/1/2 + pin |
| `fsot_quantum/scalar.py` | \(S=K(T_1+T_2+T_3)\) |
| `fsot_quantum/trinary.py` | Spin algebra + pack law |
| `fsot_quantum/device.py` | **FSOT-GPU-style** GPU/CPU adapter |
| `fsot_quantum/gates.py` / `circuit.py` | Pathway gates |
| `fsot_quantum/measure.py` | Collapse / resolve |
| `vendor/fsot_compute.py` | Pin authority |

## Twin

[FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) `fsot_lib/` — same collapse, pack, consensus ownership model.
