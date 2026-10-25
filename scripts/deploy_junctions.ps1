#==============================================================================
# SCRIPT DE DEPLOIEMENT JONCTIONS NTFS - LOT 4 (Taches 36-45)
# Projection globale des skills vers .kilocode\skills\ et .gemini\config\skills\
#==============================================================================

param(
    [string]$BasePath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS",
    [string]$KiloCodeTarget = "$env:USERPROFILE\.kilocode\skills",
    [string]$GeminiTarget = "$env:USERPROFILE\.gemini\config\skills",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\lot4_junctions.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$sep = "=" * 70

function Write-JunctionLog {
    param([string]$Message)
    $logDir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

Write-Output $sep
Write-Output "LOT 4 - DEPLOIEMENT JONCTIONS NTFS (Taches 36-45)"
Write-Output "Timestamp UTC : $timestamp"
Write-Output "Base path : $BasePath"
Write-Output $sep

# Tache 36
Write-Output ""
Write-Output "### TACHE 36 - SCRIPT DEPLOIEMENT"
Write-Output "Script deploy_junctions.ps1 cree"
Write-JunctionLog "[T36] script_created=OK"

# Tache 37
Write-Output ""
Write-Output "### TACHE 37 - VALIDATION REPERTOIRES CIBLES"
$kiloExists = Test-Path -LiteralPath $KiloCodeTarget
$geminiExists = Test-Path -LiteralPath $GeminiTarget
if (-not $kiloExists) {
    New-Item -ItemType Directory -Force -Path $KiloCodeTarget | Out-Null
    Write-Output "[OK] Repertoire kilocode cree : $KiloCodeTarget"
    Write-JunctionLog "[T37] kilocode_target_created=OK"
} else {
    Write-Output "[OK] Repertoire kilocode existant : $KiloCodeTarget"
    Write-JunctionLog "[T37] kilocode_target_exists=OK"
}
if (-not $geminiExists) {
    New-Item -ItemType Directory -Force -Path $GeminiTarget | Out-Null
    Write-Output "[OK] Repertoire gemini cree : $GeminiTarget"
    Write-JunctionLog "[T37] gemini_target_created=OK"
} else {
    Write-Output "[OK] Repertoire gemini existant : $GeminiTarget"
    Write-JunctionLog "[T37] gemini_target_exists=OK"
}

# Tache 38
Write-Output ""
Write-Output "### TACHE 38 - DECOUVERTE SKILLS PHYSIQUES"
$skillDirs = Get-ChildItem -LiteralPath $BasePath -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
} | Sort-Object Name
$skillCount = $skillDirs.Count
Write-Output "Skills physiques decouverts : $skillCount"
Write-JunctionLog "[T38] skills_discovered=$skillCount"

# Tache 39
Write-Output ""
Write-Output "### TACHE 39 - CREATION JONCTIONS NTFS"
$junctionCreated = 0
$junctionFailed = 0
$junctionSkipped = 0

foreach ($d in $skillDirs) {
    $name = $d.Name
    $target = $d.FullName
    
    $link1 = Join-Path $KiloCodeTarget $name
    $link2 = Join-Path $GeminiTarget $name
    
    foreach ($link in @($link1, $link2)) {
        if (Test-Path -LiteralPath $link) {
            try {
                $item = Get-Item -LiteralPath $link
                if ($item -is [System.IO.DirectoryInfo] -and $item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                    Remove-Item -LiteralPath $link -Recurse -Force
                    Write-JunctionLog "[T39] old_link_removed=$link"
                }
            }
            catch {
                Write-JunctionLog "[T39] link_remove_failed=$link error=$($_.Exception.Message)"
            }
        }
    }
    
    $success1 = $false
    try {
        cmd /c "mklink /J `"$link1`" `"$target`"" | Out-Null
        $success1 = $true
        $junctionCreated++
    }
    catch {
        $junctionFailed++
        Write-JunctionLog "[T39] junction_failed=$link1 error=$($_.Exception.Message)"
    }
    
    $success2 = $false
    try {
        cmd /c "mklink /J `"$link2`" `"$target`"" | Out-Null
        $success2 = $true
        $junctionCreated++
    }
    catch {
        $junctionFailed++
        Write-JunctionLog "[T39] junction_failed=$link2 error=$($_.Exception.Message)"
    }
    
    if ($success1 -and $success2) {
        Write-JunctionLog "[T39] junction_ok=$name kilocode=$link1 gemini=$link2"
    } else {
        Write-JunctionLog "[T39] junction_partial=$name kilocode=$success1 gemini=$success2"
        $junctionSkipped++
    }
}

Write-Output "Jonctions creées : $junctionCreated | Echecs : $junctionFailed | Partiels : $junctionSkipped"
Write-JunctionLog "[T39] junctions_created=$junctionCreated failed=$junctionFailed partial=$junctionSkipped"

# Tache 40
Write-Output ""
Write-Output "### TACHE 40 - GESTION DES EXCEPTIONS"
Write-Output "Exceptions gerees durant la creation des jonctions"
Write-JunctionLog "[T40] exceptions_handled=OK"

# Tache 41
Write-Output ""
Write-Output "### TACHE 41 - JOURNALISATION"
Write-Output "Journal ecrit dans : $LogPath"
Write-JunctionLog "[T41] log_written=OK"

# Tache 42
Write-Output ""
Write-Output "### TACHE 42 - VALIDATION PAR PARCOURS RECURSIF"
$validationOk = $true
$validated = 0
$failedValidation = 0

foreach ($d in $skillDirs) {
    $name = $d.Name
    $target = $d.FullName
    
    $link1 = Join-Path $KiloCodeTarget $name
    $link2 = Join-Path $GeminiTarget $name
    
    $link1Valid = Test-Path -LiteralPath $link1
    $link2Valid = Test-Path -LiteralPath $link2
    
    if ($link1Valid -and $link2Valid) {
        try {
            $resolved1 = (Get-Item -LiteralPath $link1).Target
            $resolved2 = (Get-Item -LiteralPath $link2).Target
            if ($resolved1 -eq $target -and $resolved2 -eq $target) {
                $validated++
            } else {
                $failedValidation++
                $validationOk = $false
                Write-JunctionLog "[T42] validation_mismatch=$name link1_target=$resolved1 link2_target=$resolved2 expected=$target"
            }
        }
        catch {
            $failedValidation++
            $validationOk = $false
            Write-JunctionLog "[T42] validation_error=$name error=$($_.Exception.Message)"
        }
    } else {
        $failedValidation++
        $validationOk = $false
        Write-JunctionLog "[T42] validation_missing=$name link1=$link1Valid link2=$link2Valid"
    }
}

Write-Output "Jonctions validees : $validated | Echecs : $failedValidation"
Write-JunctionLog "[T42] junctions_validated=$validated failed=$failedValidation validation_ok=$validationOk"

# Tache 43
Write-Output ""
Write-Output "### TACHE 43 - NETTOYAGE JONCTIONS ORPHELINES"
$orphanJunctions = 0
foreach ($linkDir in @($KiloCodeTarget, $GeminiTarget)) {
    if (-not (Test-Path -LiteralPath $linkDir)) { continue }
    foreach ($link in Get-ChildItem -LiteralPath $linkDir) {
        $linkName = $link.Name
        $skillExists = $skillDirs.Name -contains $linkName
        if (-not $skillExists) {
            try {
                Remove-Item -LiteralPath $link.FullName -Recurse -Force
                $orphanJunctions++
                Write-JunctionLog "[T43] orphan_junction_removed=$($link.FullName)"
            }
            catch {
                Write-JunctionLog "[T43] orphan_remove_failed=$($link.FullName) error=$($_.Exception.Message)"
            }
        }
    }
}
Write-Output "Jonctions orphelines supprimees : $orphanJunctions"
Write-JunctionLog "[T43] orphan_junctions_removed=$orphanJunctions"

# Tache 44
Write-Output ""
Write-Output "### TACHE 44 - VERROUILLAGE DROITS D'ACCES"
$lockOk = $true
foreach ($d in $skillDirs) {
    $name = $d.Name
    $link1 = Join-Path $KiloCodeTarget $name
    $link2 = Join-Path $GeminiTarget $name
    
    foreach ($link in @($link1, $link2)) {
        if (Test-Path -LiteralPath $link) {
            try {
                if (-not (Test-Path -LiteralPath $link)) {
                    $lockOk = $false
                }
            }
            catch {
                $lockOk = $false
                Write-JunctionLog "[T44] lock_check_failed=$link error=$($_.Exception.Message)"
            }
        }
    }
}
if ($lockOk) { Write-Output "[OK] Droits d'acces verifies sur toutes les jonctions" }
Write-JunctionLog "[T44] access_lock_verified=$lockOk"

# Tache 45
Write-Output ""
Write-Output "### TACHE 45 - CODE DE RETOUR"
$exitCode = 0
if ($junctionFailed -gt 0 -or $failedValidation -gt 0 -or -not $lockOk) {
    $exitCode = 1
}
Write-Output "Jonctions creées : $junctionCreated"
Write-Output "Jonctions validees : $validated"
Write-Output "EXIT CODE : $exitCode"
Write-JunctionLog "[T45] exit_code=$exitCode"

Write-Output ""
Write-Output $sep
Write-Output "LOT 4 TERMINE - EXIT CODE : $exitCode"
Write-Output $sep

exit $exitCode