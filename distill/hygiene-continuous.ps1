#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Hygiène continue — nettoyage et maintenance du système de skills ENV2 (Phase 10, T091 à T100).

.DESCRIPTION
    Exécute les opérations d'hygiène continue :
    - Nettoyage des fichiers temporaires et captures orphelines (T091)
    - Archivage des skills morts (score utilité ≤ -5) (T092)
    - Vérification de l'intégrité de skills-index.json (T093)
    - Purge des baux swarm expirés (T094)
    - Rotation des logs (T095)
    - Vérification des chemins orphelins dans les SKILL.md (T096)
    - Test de réactivation inter-shards (T097)
    - Rapport d'hygiène périodique (T098)
    - Test complet de bout en bout (T099)
    - Clôture et documentation (T100)

.PARAMETER SkillsRoot
    Répertoire racine des skills.

.PARAMETER CleanTemp
    Si spécifié, nettoie les fichiers temporaires (captures de plus de 48h).

.PARAMETER ArchiveDeadSkills
    Si spécifié, archive les skills avec score utilité ≤ -5.

.PARAMETER VerifyIndex
    Si spécifié, vérifie que skills-index.json correspond à l'état réel de skills/.

.PARAMETER PurgeExpiredLeases
    Si spécifié, marque les baux expirés dans le registre de baux.

.PARAMETER RotateLogs
    Si spécifié, rotatate les logs de plus de 7 jours.

.PARAMETER FullTest
    Si spécifié, exécute le test complet de bout en bout (T099).

.EXAMPLE
    ./hygiene-continuous.ps1 -CleanTemp -ArchiveDeadSkills -VerifyIndex -PurgeExpiredLeases -RotateLogs

.EXAMPLE
    ./hygiene-continuous.ps1 -FullTest

.NOTES
    Intégration: PHAGOCYTOSE-SPEC.md, SPEC-SKILL-FORMAT.md, skills-lifecycle-governance.md
#>

[CmdletBinding()]
param(
    [string]$SkillsRoot = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS",

    [switch]$CleanTemp,

    [switch]$ArchiveDeadSkills,

    [switch]$VerifyIndex,

    [switch]$PurgeExpiredLeases,

    [switch]$RotateLogs,

    [switch]$FullTest
)

$errors = @()
$warnings = @()
$nowUtcObj = (Get-Date).ToUniversalTime()
$nowUtc = $nowUtcObj.ToString("o")
$reportPath = Join-Path $SkillsRoot "logs" "hygiene-report-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ')).md"

if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}

# --- T091 : Nettoyage des fichiers temporaires (captures > 48h) ---
if ($CleanTemp -or $FullTest) {
    Write-Output "=== T091 : Nettoyage fichiers temporaires ==="
    $capturesDir = Join-Path $SkillsRoot "phagocytose\captures"
    if (Test-Path -LiteralPath $capturesDir) {
        $limit = $nowUtcObj.AddHours(-48)
        $old = Get-ChildItem -LiteralPath $capturesDir -File | Where-Object { $_.LastWriteTime -lt $limit }
        foreach ($f in $old) {
            Remove-Item -LiteralPath $f.FullName -Force
            Write-Output "  Supprimé : $($f.Name)"
        }
        Write-output "  Fichiers temporaires >48h supprimés : $($old.Count)"
    }
}

# --- T092 : Archivage des skills morts ---
if ($ArchiveDeadSkills -or $FullTest) {
    Write-Output "`n=== T092 : Archivage des skills morts ==="
    $skillBankDir = Join-Path $SkillsRoot "skill-bank"
    if (-not (Test-Path -LiteralPath $skillBankDir)) {
        New-Item -ItemType Directory -Force -Path $skillBankDir | Out-Null
    }
    $skillsDir = Join-Path $SkillsRoot "skills"
    if (Test-Path -LiteralPath $skillsDir) {
        $deadSkills = @()
        foreach ($folder in Get-ChildItem -LiteralPath $skillsDir -Directory) {
            $skillFile = Join-Path $folder.FullName "SKILL.md"
            if (-not (Test-Path -LiteralPath $skillFile)) { continue }
            $content = Get-Content -LiteralPath $skillFile -Raw -ErrorAction SilentlyContinue
            $content = $content -replace "^\xEF\xBB\xBF", "" -replace "`r`n", "`n"
            $match = [regex]::Match($content, '(?m)^utility_score:\s*(-?\d+)')
            if ($match.Success) {
                $score = [int]$match.Groups[1].Value
                if ($score -le -5) {
                    $deadSkills += $folder.Name
                }
            }
        }
        foreach ($dead in $deadSkills) {
            $src = Join-Path $skillsDir $dead
            $dst = Join-Path $skillBankDir $dead
            if (-not (Test-Path -LiteralPath $dst)) {
                Move-Item -LiteralPath $src -Destination $dst -Force
                Write-Output "  Archivé : $dead (score ≤ -5)"
            }
        }
        Write-output "  Skills archivés : $($deadSkills.Count)"
    }
}

# --- T093 : Vérification de l'intégrité de skills-index.json ---
if ($VerifyIndex -or $FullTest) {
    Write-Output "`n=== T093 : Vérification intégrité index ==="
    $indexPath = Join-Path $SkillsRoot "skills-index.json"
    if (Test-Path -LiteralPath $indexPath) {
        $indexContent = Get-Content -LiteralPath $indexPath -Raw -ErrorAction SilentlyContinue
        if ($indexContent) {
            try {
                $index = $indexContent | ConvertFrom-Json -ErrorAction Stop
                $skillsDir = Join-Path $SkillsRoot "skills"
                $indexedNames = @($index.skills.name)
                $missingFromIndex = @()
                foreach ($folder in Get-ChildItem -LiteralPath $skillsDir -Directory) {
                    $skillFile = Join-Path $folder.FullName "SKILL.md"
                    if (Test-Path -LiteralPath $skillFile) {
                        $content = Get-Content -LiteralPath $skillFile -Raw -ErrorAction SilentlyContinue
                        if ($content) {
                            $match = [regex]::Match($content, '(?m)^name:\s*(.+)$')
                            if ($match.Success) {
                                $name = $match.Groups[1].Value.Trim().Trim('"')
                                if ($name -and $indexedNames -notcontains $name) {
                                    $missingFromIndex += $name
                                }
                            }
                        }
                    }
                }
                if ($missingFromIndex.Count -gt 0) {
                    $warnings += "INDEX_DESYNC: $($missingFromIndex.Count) skill(s) dans skills/ absent(s) de skills-index.json : $($missingFromIndex -join ', ')"
                } else {
                    Write-Output "  Index cohérent : tous les skills actifs sont indexés."
                }
                Write-Output "  Skills indexés : $($index.skills.Count)"
            }
            catch {
                $errors += "INDEX_PARSE_ERROR: Impossible de parser skills-index.json."
            }
        }
    }
}

# --- T094 : Purge des baux swarm expirés ---
if ($PurgeExpiredLeases -or $FullTest) {
    Write-Output "`n=== T094 : Purge baux swarm expirés ==="
    $leasesPath = Join-Path $SkillsRoot "distill\leases.json"
    if (Test-Path -LiteralPath $leasesPath) {
        $leasesContent = Get-Content -LiteralPath $leasesPath -Raw -ErrorAction SilentlyContinue
        if ($leasesContent) {
            try {
                $leases = $leasesContent | ConvertFrom-Json -ErrorAction Stop
                $cleaned = 0
                foreach ($l in $leases.leases) {
                    if ($l.status -eq "active") {
                        $expires = [datetime]$l.expires_utc
                        $expires = $expires.ToUniversalTime()
                        if ($expires -lt (Get-Date).ToUniversalTime()) {
                            $l.status = "expired"
                            $cleaned++
                            Write-Output "  Bail expiré : $($l.lease_id) (territoire: $($l.territory_id))"
                        }
                    }
                }
                if ($cleaned -gt 0) {
                    $leases.generated_at_utc = $nowUtc
                    $json = $leases | ConvertTo-Json -Depth 5
                    Set-Content -LiteralPath $leasesPath -Value $json -Encoding UTF8
                }
                Write-output "  Baux expirés marqués : $cleaned"
            }
            catch {
                $errors += "LEASES_PARSE_ERROR: Impossible de parser leases.json."
            }
        }
    }
}

# --- T095 : Rotation des logs ---
if ($RotateLogs -or $FullTest) {
    Write-Output "`n=== T095 : Rotation des logs ==="
    $logDir = Join-Path $SkillsRoot "logs"
    if (Test-Path -LiteralPath $logDir) {
        $limit = $nowUtcObj.AddDays(-7)
        $old = Get-ChildItem -LiteralPath $logDir -File | Where-Object { $_.LastWriteTime -lt $limit }
        foreach ($f in $old) {
            Remove-Item -LiteralPath $f.FullName -Force
            Write-Output "  Log supprimé : $($f.Name)"
        }
        Write-output "  Logs >7j supprimés : $($old.Count)"
    }
}

# --- T096 : Vérification des chemins orphelins ---
if ($FullTest) {
    Write-Output "`n=== T096 : Vérification chemins orphelins ==="
    $skillsDir = Join-Path $SkillsRoot "skills"
    if (Test-Path -LiteralPath $skillsDir) {
        $orphanPaths = @()
        foreach ($folder in Get-ChildItem -LiteralPath $skillsDir -Directory) {
            $skillFile = Join-Path $folder.FullName "SKILL.md"
            if (-not (Test-Path -LiteralPath $skillFile)) { continue }
            $content = Get-Content -LiteralPath $skillFile -Raw -ErrorAction SilentlyContinue
            if ($content) {
                $content = $content -replace "^\xEF\xBB\xBF", "" -replace "`r`n", "`n"
                # Chercher des chemins par défaut interdits
                if ($content -match 'D:\\DO\\WEB\\TOOLS\\SKILLS\\') {
                    $orphanPaths += $folder.Name
                }
            }
        }
        if ($orphanPaths.Count -gt 0) {
            $warnings += "ORPHAN_PATHS: $($orphanPaths.Count) skill(s) avec chemin par défaut interdit : $($orphanPaths -join ', ')"
        } else {
            Write-Output "  Aucun chemin orphelin détecté."
        }
    }
}

# --- T097 : Test de réactivation inter-shards ---
if ($FullTest) {
    Write-Output "`n=== T097 : Test réactivation inter-shards ==="
    $routerScript = Join-Path $SkillsRoot "distill\skill-router.ps1"
    $indexPath = Join-Path $SkillsRoot "skills-index.json"
    if ((Test-Path -LiteralPath $routerScript) -and (Test-Path -LiteralPath $indexPath)) {
        $testResult = pwsh -File $routerScript -Request "chromium profil 2 cdp 9222" -IndexPath $indexPath -MinScore 1 -MaxResults 3 2>&1
        $testResult | Write-Output
        $lastExit = $LASTEXITCODE
        if ($lastExit -ne 0) {
            $errors += "REACTIVATION_TEST_FAIL: Le test de réactivation a échoué."
        } else {
            Write-Output "  Test de réactivation : OK"
        }
    } else {
        $warnings += "REACTIVATION_TEST_SKIP: skill-router.ps1 ou skills-index.json manquant."
    }
}

# --- T098 : Rapport d'hygiène ---
$reportLines = @()
$reportLines += "# Rapport d'hygiène continue — $nowUtc"
$reportLines += ""
$reportLines += "## Opérations effectuées"
if ($CleanTemp) { $reportLines += "- Nettoyage fichiers temporaires (T091)" }
if ($ArchiveDeadSkills) { $reportLines += "- Archivage skills morts (T092)" }
if ($VerifyIndex) { $reportLines += "- Vérification intégrité index (T093)" }
if ($PurgeExpiredLeases) { $reportLines += "- Purge baux expirés (T094)" }
if ($RotateLogs) { $reportLines += "- Rotation logs (T095)" }
if ($FullTest) {
    $reportLines += "- Vérification chemins orphelins (T096)"
    $reportLines += "- Test réactivation inter-shards (T097)"
}
$reportLines += ""
$reportLines += "## Résultats"
$reportLines += "- Erreurs : $($errors.Count)"
$reportLines += "- Avertissements : $($warnings.Count)"
$reportLines += ""
if ($warnings.Count -gt 0) {
    $reportLines += "### Avertissements"
    foreach ($w in $warnings) { $reportLines += "- $w" }
    $reportLines += ""
}
if ($errors.Count -gt 0) {
    $reportLines += "### Erreurs"
    foreach ($e in $errors) { $reportLines += "- $e" }
}

$reportContent = $reportLines -join "`n"
Set-Content -LiteralPath $reportPath -Value $reportContent -Encoding UTF8

Write-Output "`n=============================================="
Write-output "HYGIÈNE CONTINUE — RAPPORT"
Write-Output "=============================================="
Write-Output "Rapport : $reportPath"
Write-Output "Erreurs : $($errors.Count)"
Write-Output "Avertissements : $($warnings.Count)"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
}
