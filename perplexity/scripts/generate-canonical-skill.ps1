# verify_pipe.ps1 is already present — create additional helper scripts as recommended by analysis
# 1) generate-canonical-skill.ps1
# Purpose: create a canonical Perplexity skill from a template ensuring the '|' is present.
param(
    [string]$Name,
    [string]$Description,
    [string]$Title,
    [string]$Body,
    [string]$OutDir = "C:\Users\GG\Desktop\skills essai1\B"
)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

$template = @"
---
name: $Name
description: "$Description"
---
|
# $Title

$Body
"@

$filename = Join-Path $OutDir ("$Name.md")
Set-Content -Path $filename -Value $template -Encoding UTF8
Write-Output "Wrote $filename"
