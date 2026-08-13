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
| **Fold-not-Hilbert** (scale by D_eff folds, not 2^n) | green | `python -m fsot_quantum.fold_suite` |
| **Fold v2** (chem 68/68 @0.5%, GPU fold queue, surface+phase) | green | `python -m fsot_quantum.fold_v2` |
| **Fold v3** (MaxCut/Ising ledger, multi-stream, lattice surgery) | green | `python -m fsot_quantum.fold_v3` |
| **Fold v4** (mp scheduler, teleport, Gset-style, formal cost) | green | `python -m fsot_quantum.fold_v4` |
| **Fold v5** (Gset loader, multi-GPU shards, adder/QFT-role, QEMU) | green | `python -m fsot_quantum.fold_v5` |
| **Fold v6** (official G1 residual, 4-bit/modmul, GPU occupancy) | green | `python -m fsot_quantum.fold_v6` |
| **Field of use** (collapse/consensus/S on QM/QC jobs; theater labeled) | green | `python -m fsot_quantum.field_of_use` |
| **Margin vs QPU** (job residuals vs published NISQ) | green | `python -m fsot_quantum.margin_vs_qpu` |
| **Bleed refine** (Lean κ coupling + 569 atlas records ingested) | green | `python -m fsot_quantum.bleed_refine` |
| **Medium next** (T1/T2/T3 strings + Lean entanglement/QI) | green | `python -m fsot_quantum.medium_next` |
| **Keep going** (concepts + fridge/hits + 116 Lean QI/math jobs) | green | `python -m fsot_quantum.keep_going` |
| **QC/QM accuracy** (hired jobs, no fridge) | green | `python -m fsot_quantum.qc_accuracy` |
| **Bare-metal jobs** (Zig/QEMU QC-OS v0.2, 11/11) | green | `.\run_qemu.ps1` |
| **Expand sim** (Lean chem + QM replay) | green | `python -m fsot_quantum.expand_sim` |
| **Full Lean atlas** (473 files / 432 domains) | green | `python -m fsot_quantum.lean_full_atlas` |
| **Harder QC-for** (CKM / PMNS / 2D Ising / nuclear / Higgs) | **20/20 @ 0.5%** | `python -m fsot_quantum harder` |
| **Physics + QI I** | **16/16 + 326/326** | `python -m fsot_quantum qi` |
| **Physics + QI II** | **22/22 + 126/126** | `python -m fsot_quantum push` |
| **Stale-target audit** vs YR4/PDG | **20/20 @ 0.5%** | `python -m fsot_quantum audit` |
| **Physics + QI III** leftover hired physics | **41/41 + 212/212** | `python -m fsot_quantum push3` |
| **Gset family** G1–G5 + G22–G23 | **7/7 under 1%** | `python -m fsot_quantum family` |
| **Organ export** for neuron-zig | pin + \(S\) + \(\kappa\) | `python -m fsot_quantum organ` |

## Scaling law (important)

Industry QC’s hard wall is **Hilbert-space dimension / degrees of freedom**  
(amplitudes in \(\mathbb{C}^{2^n}\)). Expanding that space is the brute path.

FSOT treats complexity as **domain folds** (`D_eff` routes, collapse Θ, consensus,  
modular algebra) — same *questions* QC is sold for, different geometry of work.  
Hilbert fragments remain optional bridges; **fold path is the scaling law**.

See `docs/FOLD_NOT_HILBERT.md`.

## Wrap (2026-08-13)

The competitor climb through physics + QI III and the stale-target audit is the current wrap. Living snapshot: `docs/STATUS.md`.

What stayed open on purpose (not a retune): exclusive \(\lvert V_{cb}\rvert\), Planck vs SH0ES \(H_0\), \(\alpha_s(M_Z)\) at 0.68%, Gset champions unmatched after the <1% aspiration landed.

## Next builds (only if the wrap is reopened)

1. More official Gset only with cited champion cuts (G11 is a signed object — do not mix).
2. Exclusive \(V_{cb}\) as its own flavor-physics question, not a blend.
3. Port further Lean atlas rows only as named domain folds, never as fitted coefficients.

## How to run

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_lib.smoke_owned
python -m fsot_quantum.verify
python -m fsot_quantum.capability_suite
```

Ledgers: `results/capability_suite.json`, `results/CAPABILITY_REPORT.md`
