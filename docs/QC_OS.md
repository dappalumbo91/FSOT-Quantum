# FSOT-QC-OS — our own quantum-job OS (not a hijack)

Reality OS can host this later. **We do not need to hijack it now.**  
This image is already a tiny OS: Multiboot, no Linux, no Windows, QEMU-loadable.

## What it is

- Own kernel (`zig/src/os.zig` + `main_kernel.zig`)
- Serial is the console
- Services: core selftest + hired QC/QM job table
- Version `0.1.0`
- Apache-2.0 · pin D1D38A

## Run anywhere QEMU exists

```powershell
.\run_qemu.ps1
```

Expect:

```text
FSOT-QC-OS v0.1.0
...
JOBS 11/11
FSOT_QUANTUM_JOBS PASS
FSOT-QC-OS READY
FSOT_QUANTUM_KERNEL PASS
```

## Hosted path (Omen / Python / GPU)

Still `python -m fsot_quantum.qc_accuracy` for the wide atlas.

## Later

- Interactive serial shell (`run dj`, `run all`)
- Reality OS as an optional *host*, not a dependency
- More jobs in the table (chem/G1 stay on Python until fixed-point)

This is easier than grafting onto someone else’s OS: we already boot.
