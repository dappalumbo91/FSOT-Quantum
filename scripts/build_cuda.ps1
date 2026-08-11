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

# RTX 5070 = CC 12.0 (Blackwell). Also emit portable virtual arch.
$arch = @(
    "-gencode=arch=compute_120,code=sm_120",
    "-gencode=arch=compute_89,code=sm_89",
    "-gencode=arch=compute_86,code=sm_86"
)

Write-Host "Building smoke binary (sm_120 primary)..."
& nvcc -O3 -DFSOT_QUANTUM_MAIN @arch -o $outSmoke $src
if ($LASTEXITCODE -ne 0) {
    Write-Warning "multi-arch failed; trying sm_120 only"
    & nvcc -O3 -DFSOT_QUANTUM_MAIN -arch=sm_120 -o $outSmoke $src
    if ($LASTEXITCODE -ne 0) { throw "smoke build failed" }
}

Write-Host "Building shared DLL..."
& nvcc -O3 -shared -Xcompiler "/LD" @arch -o $outDll $src
if ($LASTEXITCODE -ne 0) {
    & nvcc -O3 -shared -Xcompiler "/LD" -arch=sm_120 -o $outDll $src
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "DLL build failed (MSVC host toolchain may be required). Smoke exe still usable."
    } else {
        Write-Host "DLL: $outDll"
    }
} else {
    Write-Host "DLL: $outDll"
}

Write-Host "Running smoke..."
& $outSmoke
if ($LASTEXITCODE -ne 0) { throw "smoke failed" }
Write-Host "CUDA path OK"
