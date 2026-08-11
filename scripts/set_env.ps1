# Environment for FSOT-Quantum CUDA builds (mirrors FSOT-GPU pattern)
$ErrorActionPreference = "Continue"

$cudaRoots = @(
    "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.3",
    "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2",
    "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8"
)
foreach ($r in $cudaRoots) {
    if (Test-Path (Join-Path $r "bin\nvcc.exe")) {
        $env:PATH = "$(Join-Path $r 'bin');$env:PATH"
        $env:CUDA_PATH = $r
        Write-Host "CUDA_PATH=$r"
        break
    }
}

# MSVC for nvcc host compiler (VS 2022)
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vswhere) {
    $vs = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ($vs) {
        $vcvars = Join-Path $vs "VC\Auxiliary\Build\vcvars64.bat"
        if (Test-Path $vcvars) {
            Write-Host "MSVC: $vs"
            cmd /c "`"$vcvars`" && set" | ForEach-Object {
                if ($_ -match "^(.*?)=(.*)$") {
                    [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
                }
            }
        }
    }
}

Write-Host "nvcc:" (Get-Command nvcc -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source)
python --version
