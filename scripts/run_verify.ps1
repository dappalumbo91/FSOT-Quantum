$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$env:PYTHONPATH = $Root
python -u -m fsot_quantum.verify
if ($LASTEXITCODE -ne 0) { throw "verify failed" }
