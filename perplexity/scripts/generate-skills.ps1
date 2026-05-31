# ============================================================
# generate-skills.ps1  v3.0
# Generate Perplexity-compliant ZIP with skill-name/SKILL.md structure
# ============================================================
param(
    [string]$SourceDir = ".\perplexity\skills",
    [string]$OutputPath = ".\perplexity\build\Skills.zip",
    [switch]$SingleSkill = $false,
    [string]$SingleSkillName = "nexus-core"
)

$ErrorActionPreference = "Stop"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

# Clean output
if (Test-Path $OutputPath) { Remove-Item $OutputPath -Force }

$tempDir = Join-Path $env:TEMP "SkillsGen_$(Get-Random)"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

if ($SingleSkill) {
    $files = Get-ChildItem -Path $SourceDir -Filter "$SingleSkillName*.md" -File
} else {
    $files = Get-ChildItem -Path $SourceDir -Filter "*.md" | Sort-Object Name
}

$processed = 0
foreach ($f in $files) {
    $name = $f.BaseName
    $raw = [System.IO.File]::ReadAllBytes($f.FullName)
    
    # Skip BOM
    $off = 0
    if ($raw.Length -ge 3 -and $raw[0] -eq 0xEF -and $raw[1] -eq 0xBB -and $raw[2] -eq 0xBF) { $off = 3 }
    $txt = [System.Text.Encoding]::UTF8.GetString($raw, $off, $raw.Length - $off)
    
    # Extract description
    $desc = ""
    if ($txt -match 'description:\s*"([^"]+)"') { $desc = $matches[1] -replace '\s+', ' ' }
    
    # Extract body after second ---
    $parts = $txt -split "---", 4
    $body = if ($parts.Count -ge 4) { $parts[3].Trim() } else { "" }
    
    # Remove ### subsections (Perplexity rule 5)
    $body = ($body -split "`n" | Where-Object { $_ -notmatch '^### ' }) -join "`n"
    
    # Create skill folder
    $skillDir = Join-Path $tempDir $name
    New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
    
    # Build clean SKILL.md
    $out = @("---", "name: $name", "description: `"$desc`"", "---", "", $body)
    [System.IO.File]::WriteAllText((Join-Path $skillDir "SKILL.md"), ($out -join "`r`n"), $utf8NoBom)
    $processed++
}

# Create ZIP
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $OutputPath, "Optimal", $false)
Remove-Item $tempDir -Recurse -Force

$z = Get-Item $OutputPath
Write-Host "Generated: $($z.Name) | $([math]::Round($z.Length/1024,1)) KB | $processed skills"