# FSOT-Quantum

**Fluid Spacetime Omni-Theory — quantum computing domain fold**

Author: **Damian Arthur Palumbo**  
License: **Apache-2.0**  
Theory authority: **[FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean)** (pin **D1D38A**)  
**Runtime authority: [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) `fsot_lib`** (vendored here)

This repository does **not** invent a second GPU stack.  
It is the **Quantum_Mechanics / Quantum_Computing** fold on the **same owned operators** already proven in FSOT-GPU:

| Operator | Module |
|----------|--------|
| Seeds / Θ = C_eff·P_var | `fsot_lib.seeds` |
| S = K(T1+T2+T3) | `fsot_lib.scalar` |
| Collapse / pack / trit similarity | `fsot_lib.trinary` |
| Coherence norm | `fsot_lib.coherence` |
| Consensus attention (no softmax) | `fsot_lib.consensus` |
| Suction–poof LR | `fsot_lib.learn` |
| Torch / native adapters | `fsot_lib.backend` |

Spins: **−1** down · **0** superposed · **+1** up.

---

## Quick start

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path

# Owned stack (FSOT-GPU)
python -m fsot_lib.smoke_owned

# Quantum fold + pin + vendor parity
python -m fsot_quantum.verify
python parity\run_parity.py
python scripts\run_demo.py

# Capability suite — QC jobs on GPU without quantum hardware
python -m fsot_quantum.capability_suite

# Next-track panels
python -c "from fsot_quantum.optimization import run_optimization_panel; print(run_optimization_panel()['overall_ok'])"
python -c "from fsot_quantum.textbook_map import run_textbook_map; print(run_textbook_map()['overall_ok'])"
python -c "from fsot_quantum.scale_scoreboard import run_scale_scoreboard; print(run_scale_scoreboard()['overall_ok'])"

# Hilbert · logical qubits · QFT/Shor · chemistry residual (compete QM/QC)
python -m fsot_quantum.compete_qm_qc

# Next steps: n=8–12 circuits · d=5/7 codes · full modular Shor · chemistry strict
python -m fsot_quantum.next_steps_suite

# Competitor climb v1: fused Hilbert n≤20 · Shor GPU · opt GPU · QAOA 11/11
python -m fsot_quantum.climb_suite

# Competitor climb v2: surface code d=3/5/7 · Shor N≤51 · mega GPU · chemistry
python -m fsot_quantum.climb_v2

# Fold-not-Hilbert: QC jobs via D_eff folds (not 2^n amplitude expansion)
python -m fsot_quantum.fold_suite

# Fold v2: chemistry 0.5% · GPU fold queue · surface+phase folds
python -m fsot_quantum.fold_v2

# Fold v3: MaxCut/Ising ledger · multi-stream scheduler · lattice surgery
python -m fsot_quantum.fold_v3

# Fold v4: multi-process · teleport sequences · Gset-style · formal cost
python -m fsot_quantum.fold_v4

# Fold v5 leftovers: official Gset loader · multi-GPU shards · adder/QFT-role · QEMU
python -m fsot_quantum.fold_v5

# Fold v6: official G1 residual · 4-bit/modular-mul folds · GPU occupancy
python -m fsot_quantum.fold_v6

# Field of use (honest): collapse/consensus/D_eff on QM/QC jobs — theater labeled
python -m fsot_quantum.field_of_use

# Margin vs published QPU field results + D_eff refine probe
python -m fsot_quantum.margin_vs_qpu

# Quantum-sector bleed (Lean connective κ) + ingest 2.1-Lean atlas headlines
python -m fsot_quantum.bleed_refine

# Water / three-string / look-snap medium + Lean entanglement/QI jobs
python -m fsot_quantum.medium_next

# Keep going: concepts + fridge/hits probe + more Lean math/QI jobs
python -m fsot_quantum.keep_going

# QC/QM accuracy board — hired jobs on ordinary hardware
python -m fsot_quantum.qc_accuracy

# QAOA exact column (must be 11/11)
python -c "from fsot_quantum.qaoa_fsot import run_qaoa_panel; r=run_qaoa_panel(); print(r['metrics_summary']); assert r['overall_ok']"

# FSOT-QC-OS v0.3.0 — standalone job OS (13 hired jobs on metal)
.\run_qemu.ps1
# interactive: .\run_qemu_stdio.ps1   (a=all c=core j=jobs h=help)

# Pull more Lean chemistry/QM atlas into this fold
python -m fsot_quantum.expand_sim

# Full Lean solved atlas (all benchmark files, not chemistry-only)
python -m fsot_quantum.lean_full_atlas

# Next stress: large MaxCut · QAOA-FSOT · textbook sim job compare
python -m fsot_quantum.stress_next

# QC questions (DJ / BV / Grover / period / factor / Ising / G1 / chem / QM)
python -m fsot_quantum.ask_qc
# or: python -m fsot_quantum ask

# Hard questions — FSOT math / K-scale, not foreign circuits (sizes 2^n cannot finish)
python -m fsot_quantum.hard_questions
# or: python -m fsot_quantum hard

# Multiprover formal stamp (Lean 4 · Coq · Isabelle · F* · Python runtime)
python scripts\run_multiprover_verification.py
# or: python -m fsot_quantum stamp

# Full skeptic kit (pin + smoke + capability + residual + textbook + scale + multiprover)
python -m fsot_quantum.skeptic_kit
# or:  .\scripts\run_skeptic_kit.ps1

# Zig twin (if zig on PATH)
cd zig; zig build run; cd ..
```

**Goal:** answers for quantum-computing *jobs* via FSOT trinary + GPU parallel — not cryogenic QPU infrastructure.

Field commands (ordinary PC):

```powershell
python -m fsot_quantum check      # pin/seeds/D_eff vs Lean clone
python -m fsot_quantum accuracy   # hired QC/QM jobs
python -m fsot_quantum ask        # QC question ledger (DJ/BV/Grover/Shor/…)
python -m fsot_quantum hard       # hard questions via K (not foreign circuits)
python -m fsot_quantum stamp      # Lean · Coq · Isabelle · F* · Python
python -m fsot_quantum atlas      # full Lean solved atlas
python -m fsot_quantum predict    # preregistered predictions (killable)
.\run_qemu.ps1                    # FSOT-QC-OS standalone
```

| Panel | Ledger |
|-------|--------|
| Capability | `results/CAPABILITY_REPORT.md` |
| Ising/MaxCut residual | `results/optimization_panel.json` |
| Textbook map | `docs/TEXTBOOK_CIRCUIT_MAP.md` |
| Scale scoreboard | `results/SCALE_SCOREBOARD.md` |
| Climb v1 | `results/CLIMB.md` |
| Climb v2 (surface + Shor mid + mega GPU) | `results/CLIMB_V2.md` |
| Fold-not-Hilbert (scaling law) | `results/FOLD_NOT_HILBERT.md` |
| Fold v2 (chem + GPU queue + phase) | `results/FOLD_V2.md` |
| Fold v3 (benchmarks + surgery + streams) | `results/FOLD_V3.md` |
| Fold v4 (mp + teleport + Gset + formal) | `results/FOLD_V4.md` |
| Fold v5 (leftovers + QEMU + paper note) | `results/FOLD_V5.md` |
| Fold v6 (official G1 + wider arith) | `results/FOLD_V6.md` |
| Field of use (honest FSOT jobs) | `results/FIELD_OF_USE.md` |
| Margin vs QPU field results | `results/MARGIN_VS_QPU.md` |
| Bleed refine (full Lean fabric) | `results/BLEED_REFINE.md` |
| Medium / three-string / QI jobs | `results/MEDIUM_NEXT.md` |
| Concepts (traceable pictures) | `docs/CONCEPTS.md` |
| Keep going (fridge probe + 116 QI jobs) | `results/KEEP_GOING.md` |
| QC/QM accuracy board | `results/QC_ACCURACY.md` |
| Bare metal / QEMU | `docs/BARE_METAL.md` |
| FSOT-QC-OS (own job OS) | `docs/QC_OS.md` |
| Expand sim (Lean chem + QM) | `results/EXPAND_SIM.md` |
| Full Lean atlas (all solved panels) | `results/LEAN_FULL_ATLAS.md` |
| Cross-check vs Lean | `results/CROSSCHECK.md` |
| QC question ledger | `results/ASK_QC.md` |
| Hard questions (K-scale) | `results/HARD_QUESTIONS.md` |
| Multiprover stamp (Lean/Coq/Isabelle/F*) | `results/MULTIPROVER_STAMP.md` |
| Preregistered predictions | `predictions/qc_preregistered.json` |
| Skeptic kit | `results/SKEPTIC_KIT.md` |

Device path is **exactly** FSOT-GPU: torch CUDA buffers when available.

---

## Layout

```
fsot_lib/                 ← FSOT-GPU owned stack (vendored)
phase1_formal_gpu/        ← Lean/Coq/Isabelle/F* trinary contracts (vendored)
phase2_native_gpu/        ← GPU engine + CUDA (vendored)
fsot_quantum/             ← Quantum domain fold only (gates, circuit, engine)
vendor/fsot_compute.py    ← pin D1D38A
config/fsot_seeds.json
parity/
results/
```

---

## Related

| Repo | Role |
|------|------|
| [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) | Theory pin |
| [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) | Owned GPU/CPU operators |
| [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) | Neural fold / bare metal |
| [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics) | Genetics fold |
| [Protofluid-Language-Translator-2.0-Zig](https://github.com/dappalumbo91/Protofluid-Language-Translator-2.0-Zig) | Language densify |

---

## License

Apache-2.0 — see [LICENSE](LICENSE).
