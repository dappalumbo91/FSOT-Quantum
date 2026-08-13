# Architecture

How this repository is put together. Capability and findings live in [`STATUS.md`](STATUS.md).

```
FSOT-2.1-Lean                 theory pin D1D38A · ~432-domain atlas
        │
        ▼
vendor/fsot_compute.py        pin file — SHA-256 prefix D1D38A
        │                     do not edit silently
        ▼
fsot_lib                      vendored from FSOT-GPU (owned operators)
  seeds / Θ = C_eff·P_var
  S = K(T1+T2+T3)
  collapse / pack / trit similarity
  coherence · consensus (no softmax) · suction–poof LR
  torch / native adapters
        │
        ▼
fsot_quantum                  this fold only
  domains   QM D=6 observed S>0
            QC D=11 unobserved S<0
            QO D=11 observed (lawful look twin)
  questions pin-wave + literature objects
  Gset      official MaxCut, KL + 2-opt
  organ     JSON readout for neuron-zig
        │
        ├── GPU (torch CUDA) when present — organ, not mind
        ├── formal/   Lean 4 · Coq · Isabelle · F*
        ├── zig/      FSOT-QC-OS under QEMU
        └── results/  living ledgers (markdown + JSON)
```

## Domain identity

| Domain | \(D_{\mathrm{eff}}\) | Looked? | \(S\) (pin) | Role |
|--------|---------------------:|:-------:|-------------|------|
| Quantum_Mechanics | 6 | yes | \(+0.9555\) | Measurement / discovery |
| Quantum_Computing | 11 | **no** | \(−0.1477\) | Dark compute |
| Quantum_Optics | 11 | yes | look twin | Lawful way to look at the compute substrate |
| Neuroscience | 14 | yes | \(+0.514\) | Mind. C_factor on T1 |
| Psychology | 16 | yes | \(+1.050\) | Walking theory of mind |
| Biology | 12 | **no** | \(+0.445\) | Living substrate, dark |

Observe path: **QC (dark) → QO (look) → QM (measure)**.  
Forcing `observed=True` on QC flips \(S\) positive and the compute identity is gone.

Bleed that matters for the mind path:

- \(\kappa(\mathrm{Neuro},\mathrm{Psych})\approx 0.080\)
- \(\kappa(\mathrm{Psych},\mathrm{QM})\approx 0.115\)
- \(\kappa(\mathrm{QC},\mathrm{Psych})\approx 0.021\) — compute may feed the mind, not be the mind
- \(\kappa(\mathrm{Bio},\mathrm{Neuro})\approx 0.034\)

## What talks to what

| Out | In | What moves |
|-----|----|------------|
| `python -m fsot_quantum organ` | fsot-neuron-zig `data/organs/fsot_quantum_organ.json` | pin, \(S\), \(\kappa\), Tsirelson, look path |
| `_ref/FSOT-2.1-Lean` | `check` / `fold` / `atlas` | pin parity + 432-domain count |
| `formal/` | `python -m fsot_quantum stamp` | five-prover OK |
| `zig/` + QEMU | `.\run_qemu.ps1` | 13 hired jobs on metal |

Zig remains **mind authority**. This fold does not speak.

phase1_formal_gpu / phase2_native_gpu = vendored from FSOT-GPU.

Device path is exactly FSOT-GPU: torch CUDA buffers when available.
