$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$env:PYTHONPATH = $Root

Write-Host "=== FSOT-Quantum skeptic kit ==="
python -m fsot_quantum.skeptic_kit
if ($LASTEXITCODE -ne 0) { throw "skeptic kit FAILED" }

# Optional Zig twin
$zig = Get-Command zig -ErrorAction SilentlyContinue
if ($zig) {
    Write-Host "=== Zig quantum twin ==="
    Push-Location (Join-Path $Root "zig")
    zig build run
    if ($LASTEXITCODE -ne 0) { Pop-Location; throw "zig twin FAILED" }
    Pop-Location
} else {
    Write-Host "zig not on PATH — skip twin"
}

Write-Host "SKEPTIC KIT PASS"
