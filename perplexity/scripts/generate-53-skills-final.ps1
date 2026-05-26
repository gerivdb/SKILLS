<#
generate-53-skills-final.ps1

Generates canonical Perplexity skill files from source .md files and packages them into a ZIP.

Behavior:
- Scan source directory (default: ./perplexity) for .md files (excluding scripts/ and examples/ by default)
- For each file, ensure canonical structure:
  - YAML frontmatter between '---' lines that contains at least 'name:' and 'description:' (if missing, create placeholders)
  - A literal block scalar '|' line immediately after the second '---'
  - A body that begins with a level-1 title '#'
  - Normalize indentation: convert leading 4-space list indent to 2 spaces
- Produce output files under build/perplexity_canonical/
- Create ZIP archive at build/perplexity_skills_final.zip
- Produce a processing report (warnings/errors)

Usage:
  cmd /c powershell -ExecutionPolicy ByPass -File "perplexity\scripts\generate-53-skills-final.ps1" [-SourceDir <path>] [-OutDir <path>] [-ZipPath <path>] [-DryRun]
#>

param(
    [string]$SourceDir = "..\..\perplexity",
    [string]$OutDir = "..\..\build\perplexity_canonical",
    [string]$ZipPath = "..\..\build\perplexity_skills_final.zip",
    [switch]$DryRun
)

Set-StrictMode -Version Latest

function Log($type, $msg) { Write-Output "[$type] $msg" }

# Resolve paths: prefer explicit path as-is (relative to current working dir), fallback to path relative to script location
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

function Resolve-InputPath([string]$p) {
    if ([string]::IsNullOrWhiteSpace($p)) { return $null }
    # If absolute or exists relative to current working dir
    if (Test-Path $p) { return (Resolve-Path -Path $p).ProviderPath }
    # Try relative to script location
    $try = Join-Path $scriptRoot $p
    if (Test-Path $try) { return (Resolve-Path -Path $try).ProviderPath }
    return $null
}

$sourceRoot = Resolve-InputPath $SourceDir
if (-not $sourceRoot) { throw "SourceDir not found: $SourceDir" }

$outRoot = Resolve-InputPath $OutDir
if (-not $outRoot) { $outRoot = Join-Path $scriptRoot $OutDir }
if (-not $DryRun) { New-Item -ItemType Directory -Path $outRoot -Force | Out-Null }

$zipDest = Resolve-InputPath $ZipPath
if (-not $zipDest) { $zipDest = Join-Path $scriptRoot $ZipPath }

# Files to exclude from generation
$excludeDirs = @('scripts','examples')

# Collect markdown files under sourceRoot, excluding excludeDirs
$mdFiles = @(Get-ChildItem -Path $sourceRoot -Recurse -File -Include *.md -ErrorAction SilentlyContinue | Where-Object {
    $rel = $_.FullName.Substring($sourceRoot.Length).TrimStart('\','/')
    $parts = $rel -split '[\\/]'
    foreach ($seg in $parts) { if ($excludeDirs -contains $seg) { return $false } }
    return $true
})

if ($mdFiles.Count -eq 0) { Log 'INFO' "No markdown files found under $sourceRoot"; exit 0 }

$report = @()

foreach ($f in $mdFiles) {
    $relPath = $f.FullName.Substring($sourceRoot.Length).TrimStart('\','/')
    $outFile = Join-Path $outRoot $relPath
    $outDir = Split-Path -Parent $outFile
    if (-not $DryRun) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

    $text = Get-Content -Raw -Encoding UTF8 -Path $f.FullName
    # Normalize CRLF
    $text = $text -replace "`r`n","`n"

    # parse frontmatter
    $lines = $text -split "`n"
    $idx = 0
    $hasFront = $false
    if ($lines.Count -gt 0 -and $lines[0].Trim() -eq '---') {
        $hasFront = $true
        $idx = 1
        while ($idx -lt $lines.Count -and $lines[$idx].Trim() -ne '---') { $idx++ }
        if ($idx -ge $lines.Count) { # no closing ---
            $hasFront = $false
        }
    }

    $warnings = New-Object System.Collections.Generic.List[String]
    $errors = New-Object System.Collections.Generic.List[String]
    if ($hasFront) {
        if ($idx -eq 1) { $frontLines = @() } else { $frontLines = $lines[1..($idx-1)] }
        if ($idx+1 -le $lines.Count-1) { $bodyLines = $lines[($idx+1)..($lines.Count-1)] } else { $bodyLines = @() }
    } else {
        # create placeholder frontmatter
        $warnings.Add("Missing frontmatter; creating placeholder") | Out-Null
        $baseName = [IO.Path]::GetFileNameWithoutExtension($f.Name)
        $frontLines = @(("name: " + $baseName), ("description: 'PLACEHOLDER description for " + $baseName + "'"))
        $bodyLines = $lines
    }

    # Ensure frontLines contain name and description
    $hasName = $false; $hasDesc = $false
    foreach ($l in $frontLines) {
        if ($l -match '^\s*name\s*:\s*(.+)$') { $hasName = $true }
        if ($l -match '^\s*description\s*:\s*(.+)$') { $hasDesc = $true }
    }
    if (-not $hasName) { $frontLines = @(("name: " + [IO.Path]::GetFileNameWithoutExtension($f.Name))) + $frontLines; $warnings.Add("Added missing 'name' in frontmatter") | Out-Null }
    if (-not $hasDesc) { $frontLines += ("description: 'PLACEHOLDER description'"); $warnings.Add("Added missing 'description' in frontmatter") | Out-Null }

    # Ensure body starts with a '# ' title
    $bodyTrim = $bodyLines | Where-Object { $_ -ne '' } | Select-Object -First 1
    if ($null -eq $bodyTrim -or -not ($bodyTrim.TrimStart() -like '#*')) {
        $warnings.Add("Body missing leading '# Title' - adding from name") | Out-Null
        $title = "# " + [IO.Path]::GetFileNameWithoutExtension($f.Name)
        $bodyLines = ,$title + $bodyLines
    }

    # Normalize indentation: replace leading 4 spaces on lines that look like list items with 2 spaces
    for ($i=0;$i -lt $bodyLines.Count;$i++) {
        $ln = $bodyLines[$i]
        if ($ln -match '^\s{4}([-*+]\s|\d+\.)') {
            $bodyLines[$i] = $ln -replace '^\s{4}','  '
        }
    }

    # Reconstruct canonical content
    $canonical = @()
    $canonical += '---'
    $canonical += $frontLines
    $canonical += '---'
    $canonical += '|'    # literal block scalar required
    $canonical += ''     # blank line for readability
    $canonical += $bodyLines

    $canonicalText = $canonical -join "`r`n"

    # Write file
    try {
        if (-not $DryRun) {
            Set-Content -Path $outFile -Value $canonicalText -Encoding UTF8 -Force
        }
        $outProvider = ''
        if (Test-Path $outFile) { $outProvider = (Resolve-Path -Path $outFile -ErrorAction SilentlyContinue).ProviderPath }
        $report += [PSCustomObject]@{
            file = $relPath
            out = $outProvider
            warnings = ($warnings -join '; ')
            errors = ($errors -join '; ')
        }
        if ($warnings.Count -gt 0) { Log 'WARN' "$relPath : $($warnings -join '; ')" }
    } catch {
        $report += [PSCustomObject]@{ file=$relPath; out=''; warnings=''; errors=$_.Exception.Message }
        Log 'ERROR' "Failed writing $outFile : $($_.Exception.Message)"
    }
}

# Ensure outRoot exists for report/zip
if (-not (Test-Path $outRoot)) { New-Item -ItemType Directory -Path $outRoot -Force | Out-Null }

# Create ZIP
if (-not $DryRun) {
    if (Test-Path $zipDest) { Remove-Item $zipDest -Force }
    $outRootFull = (Resolve-Path -Path $outRoot).ProviderPath
    Log 'INFO' "Creating ZIP $zipDest from $outRootFull"
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($outRootFull, $zipDest)
    Log 'INFO' "ZIP created: $zipDest"
}

# Write report
$reportPath = Join-Path $outRoot 'generation_report.csv'
$report | Export-Csv -Path $reportPath -NoTypeInformation -Encoding UTF8
Log 'INFO' "Report written: $reportPath"

Log 'INFO' "Processed $($report.Count) files. Zip: $zipDest"

if ($report | Where-Object { $_.errors -ne '' } ) {
    Log 'ERROR' "Some files produced errors - check generation_report.csv"
    exit 2
}

exit 0
