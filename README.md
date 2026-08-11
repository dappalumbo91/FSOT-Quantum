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

# QAOA exact column (must be 11/11)
python -c "from fsot_quantum.qaoa_fsot import run_qaoa_panel; r=run_qaoa_panel(); print(r['metrics_summary']); assert r['overall_ok']"

# Freestanding QEMU kernel (Multiboot serial gate)
.\run_qemu.ps1

# Next stress: large MaxCut · QAOA-FSOT · textbook sim job compare
python -m fsot_quantum.stress_next

# Multiprover formal stamp (Lean 4 · Coq · Isabelle · Python runtime)
python scripts\run_multiprover_verification.py

# Full skeptic kit (pin + smoke + capability + residual + textbook + scale + multiprover)
python -m fsot_quantum.skeptic_kit
# or:  .\scripts\run_skeptic_kit.ps1

# Zig twin (if zig on PATH)
cd zig; zig build run; cd ..
```

**Goal:** answers for quantum-computing *jobs* via FSOT trinary + GPU parallel — not cryogenic QPU infrastructure.

| Panel | Ledger |
|-------|--------|
| Capability | `results/CAPABILITY_REPORT.md` |
| Ising/MaxCut residual | `results/optimization_panel.json` |
| Textbook map | `docs/TEXTBOOK_CIRCUIT_MAP.md` |
| Scale scoreboard | `results/SCALE_SCOREBOARD.md` |
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
