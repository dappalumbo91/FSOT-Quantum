# FSOT-Quantum

**Fluid Spacetime Omni-Theory — alternative quantum computing on bare-metal GPU**

Author: **Damian Arthur Palumbo**  
License: **Apache-2.0**  
Theory authority: **[FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean)** (pin **D1D38A**)

This is **not** a complex-amplitude qubit simulator bolted onto CUDA.  
It is an **FSOT domain fold** for quantum capability: **trinary fluid spins** on the GPU, zero free parameters.

---

## Doctrine

| Rule | Meaning |
|------|---------|
| **One engine** | \(S = K(T_1+T_2+T_3)\) from seeds \((\pi,e,\varphi,\gamma,G)\) only |
| **Zero free parameters** | No ad-hoc fits, no Born RNG knobs, no learned gates |
| **Trinary spins** | **−1** = spin down · **0** = superposition · **+1** = spin up |
| **Collapse** | \(\Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}}\) (seed-derived) |
| **Bare metal** | CUDA kernels own pack / collapse / coupling; binary bus is transport only |

---

## Domain routing

| Domain | \(D_{\mathrm{eff}}\) | observed | Role |
|--------|---------------------:|:--------:|------|
| `Quantum_Mechanics` | 6 | yes | Spin law / measurement |
| `Quantum_Computing` | 11 | no | Compute substrate |

---

## Quick start

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path

# Pin + scalar + gate + pack + device verify (must pass)
python -m fsot_quantum.verify

# Vendor parity (byte pin D1D38A)
python parity\run_parity.py

# Host demo circuits
python scripts\run_demo.py

# Device smoke — FSOT-owned ops on torch cuda if present (NO nvcc)
python scripts\run_device_smoke.py
```

**GPU path = FSOT-GPU doctrine:** owned trinary operators; PyTorch is optional buffers/speed only.  
**Not required:** custom CUDA C++ / `nvcc` product surface.

**Hardware (optional accelerate):** NVIDIA GeForce RTX 5070 via torch CUDA when installed.

---

## Layout

```
fsot_quantum/     owned engine (seeds, scalar, trinary, gates, device adapter)
vendor/           fsot_compute.py pin authority (D1D38A)
formal/           Lean spin/pack spec
parity/           numeric twin vs vendor
docs/             math authority + pathway + architecture
results/          verify / demo / device_smoke ledgers
config/           seed triangulation JSON (FSOT-GPU twin)
cuda/             optional experiment only — NOT the product path
```

---

## Related repositories (same pin)

| Repo | Fold |
|------|------|
| [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) | Formal theory + residual atlas |
| [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) | Trinary consensus attention + LLM host |
| [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) | Neural mind bare metal |
| [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics) | Genetics / structure formulas |
| [Protofluid-Language-Translator-2.0-Zig](https://github.com/dappalumbo91/Protofluid-Language-Translator-2.0-Zig) | Language densify |

---

## What we claim / do not claim

**Claim:** A reproducible FSOT trinary quantum *pathway* — spin algebra, collapse law, domain-routed gates, host + CUDA packing — with pin-locked math and zero free parameters.

**Do not claim:** Industry QPU supremacy, full Hilbert-space equivalence to all unitary algorithms, or peer-reviewed acceptance of the broader ToE claim (that lives on FSOT-2.1-Lean).

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).

## Citation

```
Damian Arthur Palumbo. Fluid Spacetime Omni-Theory (FSOT) 2.1 — Lean verification hub.
https://github.com/dappalumbo91/FSOT-2.1-Lean

Damian Arthur Palumbo. FSOT-Quantum. https://github.com/dappalumbo91/FSOT-Quantum
```
