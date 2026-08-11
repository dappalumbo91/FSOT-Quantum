# Build freestanding FSOT-Quantum kernel and run under QEMU (serial).
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "zig")

$zigCmd = Get-Command zig -ErrorAction SilentlyContinue
$zig = $null
if ($zigCmd) { $zig = $zigCmd.Source }
if (-not $zig) {
    $cand = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter zig.exe -Recurse -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
    if ($cand) { $zig = $cand }
}
if (-not $zig) { throw "zig not found on PATH" }

Write-Host "=== zig build kernel ==="
& $zig build kernel
if ($LASTEXITCODE -ne 0) { throw "zig build kernel failed" }

$binDir = Join-Path (Get-Location) "zig-out\bin"
$kernelSrc = Join-Path $binDir "fsot_quantum_kernel"
if (-not (Test-Path $kernelSrc)) {
    $alt = Get-ChildItem $binDir -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "fsot_quantum_kernel*" } | Select-Object -First 1
    if ($alt) { $kernelSrc = $alt.FullName }
}
if (-not (Test-Path $kernelSrc)) { throw "kernel binary missing in zig-out\bin" }

$qemu = $null
$q = Get-Command qemu-system-x86_64 -ErrorAction SilentlyContinue
if ($q) { $qemu = $q.Source }
if (-not $qemu) {
    $qpath = "C:\Program Files\qemu\qemu-system-x86_64.exe"
    if (Test-Path $qpath) { $qemu = $qpath }
}
if (-not $qemu) {
    Write-Host "WARN: qemu not found - kernel at $kernelSrc"
    exit 0
}

$kernel = Join-Path $env:TEMP "fsot_quantum_kernel"
$serialLog = Join-Path $env:TEMP "fsot_quantum_qemu_serial.log"
$errLog = Join-Path $env:TEMP "fsot_quantum_qemu_err.log"
Copy-Item -Force $kernelSrc $kernel
Remove-Item $serialLog -ErrorAction SilentlyContinue
Remove-Item $errLog -ErrorAction SilentlyContinue

Write-Host "=== QEMU serial ==="
$argList = @(
    "-display", "none",
    "-serial", "file:$serialLog",
    "-no-reboot",
    "-m", "64M",
    "-kernel", $kernel
)
$p = Start-Process -FilePath $qemu -ArgumentList $argList -PassThru -WindowStyle Hidden -RedirectStandardError $errLog
Start-Sleep -Seconds 12
if (-not $p.HasExited) {
    Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
}

Write-Host "--- serial ---"
if (Test-Path $serialLog) {
    Get-Content $serialLog
    $txt = Get-Content $serialLog -Raw
    $resDir = Join-Path $PSScriptRoot "results"
    New-Item -ItemType Directory -Force -Path $resDir | Out-Null
    Copy-Item -Force $serialLog (Join-Path $resDir "qemu_serial.log")
    if ($txt -match "FSOT_QUANTUM_KERNEL PASS") {
        Write-Host "=== QEMU GATE PASS ==="
        exit 0
    }
    Write-Host "=== QEMU GATE FAIL ==="
    exit 1
}

Write-Host "no serial log"
if (Test-Path $errLog) { Get-Content $errLog }
exit 1
