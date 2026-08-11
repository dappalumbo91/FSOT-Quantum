# Alternative quantum computing pathway (FSOT)

## What this is

An **FSOT-native** quantum *capability* — not a simulator of industry gate-model qubits on \(\mathbb{C}^{2^n}\), and **not** a custom-CUDA science project.

## GPU doctrine (same as FSOT-GPU)

| Layer | Role |
|-------|------|
| **Owned operators** | collapse `Θ=C_eff·P_var`, trinary pack, neg/CX/consensus, scalar `S` |
| **Device adapter** | optional **PyTorch** buffers on `cuda` if present — **speed only** |
| **Custom `.cu` / nvcc** | **not required** for this pathway |

FSOT-GPU already proved sparse trinary consensus and pack on device **without** making nvcc the product surface. This repo follows that:

```text
fsot_quantum/trinary.py   — law
fsot_quantum/device.py    — torch-or-python adapter (prefer_device)
scripts/run_device_smoke.py
```

Industry quantum stacks (cuQuantum, Qiskit Aer GPU, …) are **not** the spine.

## Spins

\[
\mathbb{T} = \{-1,\,0,\,+1\}
\]

| Value | Name |
|------:|------|
| \(+1\) | Spin up |
| \(0\) | Superposition |
| \(-1\) | Spin down |

## Domains

| Domain | \(D_{\mathrm{eff}}\) | observed | Role |
|--------|---------------------:|:--------:|------|
| `Quantum_Mechanics` | 6 | yes | Spin law / measure |
| `Quantum_Computing` | 11 | no | Compute substrate |

## Gate set

| Gate | Law |
|------|-----|
| X | `neg(t) = -t` |
| Z | `pair(t, phase_class(S_domain))` |
| H | poles → superposed; superposed → `sign(S)` |
| CX | control +1 flip; 0 super; −1 hold |
| … | see `fsot_quantum/gates.py` |

## Measurement

1. Continuous field → `collapse` with \(\Theta\).  
2. Discrete superposed → `sign(S(domain))`.  
3. \(\pm 1\) eigenstates fixed under measure.

## What about `cuda/`?

Left only as an **optional** experimental note for people who already compile FSOT-GPU kernels. **Default path never needs it.** Prefer:

```powershell
python scripts\run_device_smoke.py
python -m fsot_quantum.verify
```
