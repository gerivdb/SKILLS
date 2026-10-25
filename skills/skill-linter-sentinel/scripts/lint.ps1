#==============================================================================
# SKILL: skill-linter-sentinel
# Rôle: Linter continu pour skills L4 (encodage CP1252, syntaxe Python/PowerShell).
# Couche: Méta-Skills & Cycle de Vie
#==============================================================================

[CmdletBinding()]
param(
    [string]$SkillPath = ".",
    [switch]$CheckEncoding = $true,
    [switch]$CheckPython = $true,
    [switch]$CheckPowerShell = $true,
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\lint-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$errors = @()
$warnings = @()

function Write-WAL {
    param([string]$Message)
    $logDir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# Fonction pour vérifier l'encodage d'un fichier
function Test-Cp1252Encoding {
    param([string]$FilePath)
    try {
        $bytes = [System.IO.File]::ReadAllBytes($FilePath)
        $utf8 = [System.Text.Encoding]::UTF8
        $decoded = $utf8.GetString($bytes)
        # Vérifier s'il y a des caractères suspects (émojis, etc.)
        foreach ($c in $decoded.ToCharArray()) {
            if ([int]$c -gt 127) {
                $warnings += [PSCustomObject]@{
                    File   = $FilePath
                    Type   = "Non-ASCII character"
                    Detail = "Caractère U+$([int]$c.ToString('X4)) : $c"
                }
            }
        }
        return $true
    }
    catch {
        $errors += [PSCustomObject]@{
            File   = $FilePath
            Type   = "Encoding error"
            Detail = $_.Exception.Message
        }
        return $false
    }
}

# Fonction pour valider la syntaxe Python
function Test-PythonSyntax {
    param([string]$FilePath)
    try {
        $null = python -c "import py_compile; py_compile.compile(r'$FilePath', doraise=True)"
        return $true
    }
    catch {
        $errors += [PSCustomObject]@{
            File   = $FilePath
            Type   = "Python syntax error"
            Detail = $_.Exception.Message
        }
        return $false
    }
}

# Fonction pour valider la syntaxe PowerShell
function Test-PowerShellSyntax {
    param([string]$FilePath)
    try {
        $errorsParser = $null
        $null = [System.Management.Automation.Language.Parser]::ParseFile($FilePath, [ref]$null, [ref]$errorsParser)
        if ($errorsParser -and $errorsParser.Count -gt 0) {
            foreach ($e in $errorsParser) {
                $errors += [PSCustomObject]@{
                    File   = $FilePath
                    Type   = "PowerShell parse error"
                    Detail = $e.Message
                }
            }
            return $false
        }
        return $true
    }
    catch {
        $errors += [PSCustomObject]@{
            File   = $FilePath
            Type   = "PowerShell parse exception"
            Detail = $_.Exception.Message
        }
        return $false
    }
}

# Auditer le skill
if (-not (Test-Path -LiteralPath $SkillPath)) {
    Write-Output "[FAIL] Chemin introuvable : $SkillPath"
    Write-Wal "[FAIL] Chemin introuvable : $SkillPath"
    exit 1
}

Write-Output "[LINT] Audit du skill : $SkillPath"
Write-Wal "[LINT] Début audit : $SkillPath"

# Vérifier SKILL.md
$skillMd = Join-Path $SkillPath "SKILL.md"
if (Test-Path -LiteralPath $skillMd) {
    if ($CheckEncoding) { Test-Cp1252Encoding -FilePath $skillMd }
    # Vérifier le frontmatter
    $content = Get-Content -LiteralPath $skillMd -Raw -ErrorAction SilentlyContinue
    if ($content -notmatch "^---") {
        $warnings += [PSCustomObject]@{
            File   = $skillMd
            Type   = "Missing frontmatter"
            Detail = "SKILL.md sans frontmatter YAML"
        }
    }
}

# Auditer les scripts
$scriptsDir = Join-Path $SkillPath "scripts"
if (Test-Path -LiteralPath $scriptsDir) {
    $scripts = Get-ChildItem -LiteralPath $scriptsDir -File -Recurse
    foreach ($script in $scripts) {
        $ext = $script.Extension.ToLower()
        if ($ext -eq ".ps1" -and $CheckPowerShell) {
            Test-PowerShellSyntax -FilePath $script.FullName
            if ($CheckEncoding) { Test-Cp1252Encoding -FilePath $script.FullName }
        }
        elseif ($ext -eq ".py" -and $CheckPython) {
            Test-PythonSyntax -FilePath $script.FullName
        }
    }
}

# Rapport
$report = [PSCustomObject]@{
    Timestamp  = $timestamp
    SkillPath  = $SkillPath
    Errors     = $errors.Count
    Warnings   = $warnings.Count
    ErrorList  = $errors
    WarningList = $warnings
    Status     = if ($errors.Count -eq 0) { "OK" } else { "FAIL" }
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[LINT] Fin audit : $SkillPath errors=$($errors.Count) warnings=$($warnings.Count)"

if ($errors.Count -gt 0) {
    exit 1
}
exit 0