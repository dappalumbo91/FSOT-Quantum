# Build FSOT-Quantum CUDA kernels (RTX / CUDA 13.x)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$nvcc = Get-Command nvcc -ErrorAction SilentlyContinue
if (-not $nvcc) {
    Write-Error "nvcc not on PATH. Run scripts\set_env.ps1 first."
}

$outDll = Join-Path $Root "cuda\fsot_quantum_cuda.dll"
$outSmoke = Join-Path $Root "cuda\fsot_quantum_smoke.exe"
$src = Join-Path $Root "cuda\fsot_quantum.cu"

Write-Host "Building smoke binary..."
& nvcc -O3 -DFSOT_QUANTUM_MAIN -o $outSmoke $src
if ($LASTEXITCODE -ne 0) { throw "smoke build failed" }

Write-Host "Building shared DLL..."
& nvcc -O3 -shared -Xcompiler "/LD" -o $outDll $src
if ($LASTEXITCODE -ne 0) {
    Write-Warning "DLL build failed (MSVC host toolchain may be required). Smoke exe still usable."
} else {
    Write-Host "DLL: $outDll"
}

Write-Host "Running smoke..."
& $outSmoke
if ($LASTEXITCODE -ne 0) { throw "smoke failed" }
Write-Host "CUDA path OK"
