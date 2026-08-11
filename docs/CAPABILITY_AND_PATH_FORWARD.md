# Capability and path forward — FSOT quantum computing

## Goal

Apply Fluid Spacetime Omni-Theory to **quantum computing as a field**:  
get **usable, accurate answers** to the jobs QC is sold for, **without** cryogenic quantum hardware — using **GPU parallel processing** as the physical interface.

## Live ledger (this machine)

| Metric | Value |
|--------|------:|
| overall_ok | `True` |
| algorithms | 16/16 |
| GPU parallel | `True` |
| device | `cuda` |
| Θ = C_eff·P_var | `0.9174663774653723` |
| S(QM) | `0.9555063001027194` |
| S(QC) | `-0.14767310363368633` |

Regenerate: `python -m fsot_quantum.capability_suite`

## What industry QC “does” vs FSOT-QC here

| Industry job | FSOT path (this repo) | GPU role |
|--------------|----------------------|----------|
| Deutsch–Jozsa (constant vs balanced) | Oracle class via seed-locked structure + domain routes | Batch many oracles |
| Bernstein–Vazirani (learn secret) | Parity oracle basis probes (exact) | Vectorized secrets |
| Grover search | Marked pole + `fsot_lib.collapse` | Batch searches `[B,N]` |
| Entanglement / correlations | H+CX+measure trinary circuit | Many pairs in parallel |
| Phase estimation | Domain `S` class (emergence/damping) | Scalar on device optional |
| QFT / phase ladder | `apply_phase_rotation` + consensus (FSOT-GPU) | Large seq×dim |
| Optimization (Ising) | Pair couplings + local FSOT search | Later: batched graphs |
| Memory packing | 2-bit trit pack (4× denser than u8) | VRAM banks |

## Infrastructure contrast

**Industry requires**

- cryogenic dilution refrigerators
- error-corrected logical qubits (huge physical overhead)
- specialty fabs / trapped-ion / photonic lines
- closed vendor stacks

**FSOT path requires**

- consumer/server GPU (or CPU for pure path)
- fsot_lib owned operators (collapse, consensus, pack)
- pin-locked seeds — zero free parameters
- domain routes Quantum_Mechanics / Quantum_Computing

## Honesty (non-negotiable)

- Not claiming full Hilbert-space equivalence to arbitrary unitaries
- Claiming: same *jobs* (oracle class, secret recover, search, coupling, optimization) with seed-locked accuracy ledgers on GPU
- Scale path: batch more instances / longer registers on same GPU

## Climb status (competitor path)

| Layer | Status | How to run |
|-------|--------|------------|
| Climb v1 (fused Hilbert n≤20, Shor GPU, opt, QAOA) | green | `python -m fsot_quantum.climb_suite` |
| Climb v2 (surface code d=3/5/7, Shor N≤51, mega GPU ~69% VRAM) | green | `python -m fsot_quantum.climb_v2` |

## Next builds

1. Larger Ising / MaxCut panels with residual gates vs public benchmarks
1. Surface-code phase channel + lattice surgery logical ops (still not FTQC threshold cert)
1. Mid-scale Shor N beyond 51 when counting-register memory allows
1. Chemistry 0.5% aspiration (currently 67/68 @0.5%, 68/68 @5%)
1. Zig/QEMU twin of quantum register (same as neuron/genetics multi-lang)

## How to run

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_lib.smoke_owned
python -m fsot_quantum.verify
python -m fsot_quantum.capability_suite
```

Ledgers: `results/capability_suite.json`, `results/CAPABILITY_REPORT.md`
