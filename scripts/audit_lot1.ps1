#==============================================================================
# SCRIPT D'AUDIT COMPLET - LOT 1 (Taches 1-10)
#==============================================================================

param(
    [string]$BasePath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS",
    [string]$AuditLog = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\audit_lot1_intermediate.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$sep = "=" * 70

function Write-AuditLog {
    param([string]$Message)
    "$timestamp | $Message" | Out-File -FilePath $AuditLog -Append -Encoding UTF8
}

Write-Output $sep
Write-Output "LOT 1 - AUDIT PROFOND (Taches 1-10)"
Write-Output "Timestamp UTC : $timestamp"
Write-Output "Base path : $BasePath"
Write-Output $sep

# Tache 1
Write-Output ""
Write-Output "### TACHE 1 - SCAN RECURSIF"
$skillDirs = Get-ChildItem -LiteralPath $BasePath -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
} | Sort-Object Name
$physicalCount = $skillDirs.Count
Write-Output "Skills physiques : $physicalCount"
Write-AuditLog "[T1] physical_skills_count=$physicalCount"

# Tache 2
Write-Output ""
Write-Output "### TACHE 2 - VALIDATION YAML"
$yamlValid = 0
$yamlInvalid = 0
foreach ($d in $skillDirs) {
    $skillMd = Join-Path $d.FullName "SKILL.md"
    $content = Get-Content -LiteralPath $skillMd -Raw -ErrorAction SilentlyContinue
    if (-not $content) {
        $yamlInvalid++
        Write-Output "[FAIL] $($d.Name) : illisible"
        continue
    }
    if ($content -match "^---" -and $content -match "type:\s*SKILL") {
        $yamlValid++
    } else {
        $yamlInvalid++
        Write-Output "[FAIL] $($d.Name) : frontmatter invalide"
    }
}
Write-Output "Valides : $yamlValid | Invalides : $yamlInvalid"
Write-AuditLog "[T2] yaml_valid=$yamlValid yaml_invalid=$yamlInvalid"

# Tache 3
Write-Output ""
Write-Output "### TACHE 3 - METADONNEES"
$skillMetadata = @()
foreach ($d in $skillDirs) {
    $skillMd = Join-Path $d.FullName "SKILL.md"
    $content = Get-Content -LiteralPath $skillMd -Raw -ErrorAction SilentlyContinue
    $name = $d.Name
    $version = "unknown"
    $status = "unknown"
    $intentHash = "unknown"
    if ($content -match 'version:\s*"([^"]+)"') { $version = $matches[1] }
    if ($content -match 'status:\s*(\S+)') { $status = $matches[1] }
    if ($content -match 'intent_hash:\s*(0x[0-9A-Fa-f]+)') { $intentHash = $matches[1] }
    $skillMetadata += [PSCustomObject]@{
        Name       = $name
        Version    = $version
        Status     = $status
        IntentHash = $intentHash
    }
}
Write-Output "Metadonnees extraites : $($skillMetadata.Count)"
Write-AuditLog "[T3] metadata_extracted=$($skillMetadata.Count)"

# Tache 4
Write-Output ""
Write-Output "### TACHE 4 - ORPHELINS PHYSIQUES"
$registryPath = Join-Path $BasePath "REGISTRY.yaml"
$registryContent = Get-Content -LiteralPath $registryPath -Raw -ErrorAction SilentlyContinue
$registryIds = @()
if ($registryContent) {
    $matches = [regex]::Matches($registryContent, "- id:\s*(\S+)")
    foreach ($m in $matches) { $registryIds += $m.Groups[1].Value }
}
$registryCount = $registryIds.Count
Write-Output "Entrees registre : $registryCount"

$orphanPhysical = $skillDirs | Where-Object { $registryIds -notcontains $_.Name }
$orphanCount = $orphanPhysical.Count
Write-Output "Orphelins physiques : $orphanCount"
foreach ($o in $orphanPhysical) { Write-Output "  [ORPHAN] $($o.Name)" }
Write-AuditLog "[T4] orphan_physical=$orphanCount"

# Tache 5
Write-Output ""
Write-Output "### TACHE 5 - PARSING REGISTRY"
Write-Output "IDs extraits : $registryCount"
Write-AuditLog "[T5] registry_ids_count=$registryCount"

# Tache 6
Write-Output ""
Write-Output "### TACHE 6 - ENTITES FANTOMES"
$ghostRegistry = $registryIds | Where-Object { $skillDirs.Name -notcontains $_ }
$ghostCount = $ghostRegistry.Count
Write-Output "Entites fantomes : $ghostCount"
foreach ($g in $ghostRegistry) { Write-Output "  [GHOST] $g" }
Write-AuditLog "[T6] ghost_registry=$ghostCount"

# Tache 7
Write-Output ""
Write-Output "### TACHE 7 - ECARTS TOPOLOGIQUES"
$auditReport = [PSCustomObject]@{
    Timestamp       = $timestamp
    PhysicalSkills  = $physicalCount
    RegistryEntries = $registryCount
    OrphanPhysical  = $orphanCount
    GhostRegistry   = $ghostCount
    YamlValid       = $yamlValid
    YamlInvalid     = $yamlInvalid
}
$auditReport | ConvertTo-Json -Depth 3 | Out-File -FilePath (Join-Path $BasePath "audit_lot1_report.json") -Encoding UTF8
Write-Output "Rapport : audit_lot1_report.json"
Write-AuditLog "[T7] report_written=OK"

# Tache 8
Write-Output ""
Write-Output "### TACHE 8 - PERMISSIONS NTFS"
$ntfsOk = $true
foreach ($d in $skillDirs) {
    $acl = Get-Acl -LiteralPath $d.FullName -ErrorAction SilentlyContinue
    if (-not $acl) {
        $ntfsOk = $false
        Write-Output "[FAIL] $($d.Name) : ACL illisible"
    }
}
if ($ntfsOk) { Write-Output "[OK] ACL NTFS lisibles" }
Write-AuditLog "[T8] ntfs_ok=$ntfsOk"

# Tache 9
Write-Output ""
Write-Output "### TACHE 9 - ESPACE DISQUE"
$driveD = Get-PSDrive -Name D -ErrorAction SilentlyContinue
$driveC = Get-PSDrive -Name C -ErrorAction SilentlyContinue
if ($driveD) {
    $freeD = [math]::Round($driveD.Free / 1GB, 2)
    $totalD = [math]::Round($driveD.Size / 1GB, 2)
    Write-Output "D: $freeD Go / $totalD Go"
    Write-AuditLog "[T9] driveD_free_GB=$freeD driveD_total_GB=$totalD"
}
if ($driveC) {
    $freeC = [math]::Round($driveC.Free / 1GB, 2)
    $totalC = [math]::Round($driveC.Size / 1GB, 2)
    Write-Output "C: $freeC Go / $totalC Go"
    Write-AuditLog "[T9] driveC_free_GB=$freeC driveC_total_GB=$totalC"
}

# Tache 10
Write-Output ""
Write-Output "### TACHE 10 - CODE DE RETOUR"
$exitCode = 0
if ($yamlInvalid -gt 0) { $exitCode = 1 }
if ($orphanCount -eq 0 -and $ghostCount -eq 0) {
    Write-Output "Etat parfaitement synchronise"
} else {
    Write-Output "Ecarots : $orphanCount orphelins, $ghostCount fantomes"
}
Write-AuditLog "[T10] exit_code=$exitCode"

Write-Output ""
Write-Output $sep
Write-Output "LOT 1 TERMINE - EXIT CODE : $exitCode"
Write-Output $sep

exit $exitCode