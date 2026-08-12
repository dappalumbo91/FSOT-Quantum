# Bare metal + host — how this actually runs

**Goal:** load on anyone’s machine. No fridge. No other OS required for the *core jobs*.  
Python/GPU stays as a **hosted** path (HP Omen, CUDA). Zig/QEMU is the **standalone** path.

## Two stacks, one engine

| Path | Needs | What it answers |
|------|--------|------------------|
| **Zig Multiboot kernel** (`zig/src/`) | QEMU (or later Reality OS / raw metal) | Hired QC/QM *jobs* in integer core + serial ledger |
| **Python + GPU** (`fsot_quantum/`) | Python, optional CUDA | Same jobs + chemistry 68/68, G1, Lean replay, big GPU batches |

Same pin **D1D38A**. Same trits. Same Θ milli 917. Same fold-budget lemma.

## How to run standalone (any PC with QEMU)

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
.\run_qemu.ps1
```

Serial should end with:

```text
JOBS 9/9
FSOT_QUANTUM_JOBS PASS
FSOT_QUANTUM_KERNEL PASS
```

Jobs on metal: DJ, BV, search, period, factor, Ising, CHSH, domain signs, fold-vs-Hilbert.

## How to run hosted (this Omen / any Python box)

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.qc_accuracy
```

## Later

Drop the same kernel into **FSOT Reality OS** — not now. The kernel is already OS-less (Multiboot).

## Honesty

Chemistry 68/68 and Gset G1 are **not** in the kernel yet (float / file I/O).  
The kernel is the mechanical job core. Host Python is the wide ledger. Both are real; neither is theater.
