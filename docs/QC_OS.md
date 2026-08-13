# FSOT-QC-OS — our own quantum-job OS (not a hijack)

Reality OS can host this later. **We do not need to hijack it now.**  
This image is already a tiny OS: Multiboot, no Linux, no Windows, QEMU-loadable.

## What it is

- Own kernel (`zig/src/os.zig` + `main_kernel.zig`)
- Serial is the console
- Services: core selftest + hired QC/QM job table
- Version `0.2.0` (serial shell: a/c/j/h; file-serial defaults to all)
- Apache-2.0 · pin D1D38A

## Run anywhere QEMU exists

```powershell
.\run_qemu.ps1
```

Expect:

```text
FSOT-QC-OS v0.2.0
SHELL a=all c=core j=jobs h=help
CMD a
...
JOBS 11/11
FSOT-QC-OS READY
```

Interactive: `.\run_qemu_stdio.ps1`

## Hosted path (Omen / Python / GPU)

Still `python -m fsot_quantum.qc_accuracy` for the wide atlas.

## Later

- Interactive serial shell (`run dj`, `run all`)
- Reality OS as an optional *host*, not a dependency
- More jobs in the table (chem/G1 stay on Python until fixed-point)

This is easier than grafting onto someone else’s OS: we already boot.
