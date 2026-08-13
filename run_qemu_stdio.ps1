# Interactive FSOT-QC-OS (serial on stdio). Type a / c / j / h then Enter.
# One-shot CI path remains .\run_qemu.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "zig")
$zig = (Get-Command zig -ErrorAction SilentlyContinue).Source
if (-not $zig) { throw "zig not found" }
& $zig build kernel
if ($LASTEXITCODE -ne 0) { throw "zig build kernel failed" }
$kernel = Join-Path (Get-Location) "zig-out\bin\fsot_quantum_kernel"
$qemu = "C:\Program Files\qemu\qemu-system-x86_64.exe"
if (-not (Test-Path $qemu)) { $qemu = (Get-Command qemu-system-x86_64).Source }
& $qemu -display none -serial stdio -no-reboot -m 64M -kernel $kernel
