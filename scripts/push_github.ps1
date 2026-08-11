# Push FSOT-Quantum to GitHub over HTTPS (no gh auth required if credential helper / token works).
# Usage:
#   .\scripts\push_github.ps1
#   .\scripts\push_github.ps1 -Token $env:GITHUB_TOKEN
#   .\scripts\push_github.ps1 -RepoName FSOT-Quantum

param(
    [string]$RepoName = "FSOT-Quantum",
    [string]$Owner = "dappalumbo91",
    [string]$Token = $env:GITHUB_TOKEN,
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Test-Path ".git")) {
    git init -b $Branch
}

git add -A
$status = git status --porcelain
if ($status) {
    git commit -m "FSOT-Quantum: trinary spin pathway on bare-metal GPU (pin D1D38A, zero free params)"
} else {
    Write-Host "No new changes to commit."
}

$remoteUrl = "https://github.com/$Owner/$RepoName.git"
$authUrl = $remoteUrl
if ($Token) {
    $authUrl = "https://$Token@github.com/$Owner/$RepoName.git"
}

# Create repo via API if token present and repo missing
if ($Token) {
    $headers = @{
        Authorization = "Bearer $Token"
        Accept        = "application/vnd.github+json"
        "User-Agent"  = "FSOT-Quantum-push"
    }
    try {
        Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$RepoName" -Headers $headers -Method Get | Out-Null
        Write-Host "Remote repo exists: $Owner/$RepoName"
    } catch {
        Write-Host "Creating public repo $Owner/$RepoName ..."
        $body = @{
            name        = $RepoName
            description = "FSOT alternative quantum computing — trinary spins on bare-metal GPU. Pin D1D38A. Zero free parameters."
            private     = $false
            auto_init   = $false
        } | ConvertTo-Json
        Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType "application/json" | Out-Null
    }
}

$existing = git remote 2>$null
if ($existing -notcontains "origin") {
    git remote add origin $remoteUrl
} else {
    git remote set-url origin $remoteUrl
}

Write-Host "Pushing to $remoteUrl ..."
if ($Token) {
    git push -u $authUrl "HEAD:$Branch"
    # scrub token from remote url
    git remote set-url origin $remoteUrl
} else {
    # Uses Windows Credential Manager / interactive HTTPS if available
    git push -u origin $Branch
}

Write-Host "Done. https://github.com/$Owner/$RepoName"
