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

## Next builds — status

| Item | Status | Where |
|------|--------|--------|
| Ising / MaxCut residual panels | **Done** (13/13 exact, n≤16) | `results/optimization_panel.json` |
| Textbook circuit map | **Done** (13/13) | `docs/TEXTBOOK_CIRCUIT_MAP.md` |
| Scale / throughput scoreboard | **Done** (GPU) | `results/SCALE_SCOREBOARD.md` |
| Zig quantum register twin | **Done** | `zig/` · `zig build run` |
| Skeptic one-command kit | **Done** | `python -m fsot_quantum.skeptic_kit` |
| GitHub publish | **Open** (HTTPS token needed) | `scripts/push_github.ps1` |

### Still open

1. Larger MaxCut banks (n>16) with approximate + certified bounds  
2. QEMU freestanding twin (neuron-style ladder)  
3. arXiv-style methods note with ledgers  

## How to run

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.skeptic_kit
# or full script including Zig:
.\scripts\run_skeptic_kit.ps1
```

Ledgers: `results/skeptic_kit.json`, `results/capability_suite.json`, `results/optimization_panel.json`, `results/scale_scoreboard.json`
