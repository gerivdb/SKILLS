---
name: reposcope-compare
version: "1.0"
intent_hash: 0xSKILL_REPOSCOPE_COMPARE_20260615
---

# Skill: reposcope-compare

## Quand l'utiliser

- L'utilisateur veut exécuter le pipeline complet REPOSCOPE-COMPARE sur un repo externe
- ECOS-CLI `reposcope-compare <owner>/<repo>` est appelé

**NE PAS utiliser** pour des analyses partielles (utiliser les skills individuels à la place).

## Références

- **INTENT** : INTENT-041e (GOVERNANCE-HUB)
- **PRD** : PRD-REPOSCOPE-PIPELINE-2026-06-15
- **EPIC** : EPIC-REPOSCOPE-PIPELINE

## Pipeline orchestré

### Étape 1 — Valider l'entrée

```powershell
param(
    [Parameter(Mandatory=$true)] [string] $RepoUrl
)

if ($RepoUrl -notmatch '^[\w-]+/[\w-]+$') {
    Write-Output "[ERROR] URL invalide. Format attendu: <owner>/<repo>"
    exit 1
}
```

### Étape 2 — Gestion du lock file (prévention des exécutions concurrentes)

```powershell
$slug = $RepoUrl.Replace("/", "_")
$lockPath = "C:\DevTools\bin\.locks\reposcope_${slug}.lock"
$lockDir = Split-Path $lockPath

if (-not (Test-Path $lockDir)) {
    New-Item -ItemType Directory -Path $lockDir -Force | Out-Null
}

if (Test-Path $lockPath) {
    $lockTime = (Get-Item $lockPath).LastWriteTime
    if ((Get-Date) - $lockTime -lt (New-TimeSpan -Hours 24)) {
        Write-Output "[ERROR] Un autre processus traite déjà ce repo. Lock file: $lockPath"
        exit 3
    } else {
        # Lock périmé (>24h), le supprimer
        Remove-Item $lockPath -Force
    }
}

# Créer le lock
New-Item -ItemType File -Path $lockPath -Value (Get-Date -Format "o") | Out-Null

try {
    # ... [pipeline] ...
} finally {
    # Toujours supprimer le lock à la fin
    if (Test-Path $lockPath) {
        Remove-Item $lockPath -Force
    }
}
```

### Étape 3 — Pipeline séquentiel

```powershell
Write-Output "[reposcope-compare] Démarrage pipeline pour $RepoUrl"
$startTime = Get-Date

# GATE-0 — Chargement SOT (cache dans compétences)
Write-Output "[reposcope-compare] GATE-0: Chargement SOT..."
# Les skills individuels chargent leurs propres SOT avec cache

# ÉTAPE 1 — EXTRACT
Write-Output "[reposcope-compare] ÉTAPE 1: EXTRACTION"
$extractOutput = & {
    # Appel au skill reposcope-extract via le mécanisme Kilo
    # En pratique : cela serait fait via une invocation de skill ou un script wrapper
    # Pour ce skill, nous décrivons la logique
    $extractPath = "NEXUS/reposcope/extract_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    # Simuler l'appel : en réalité, ce serait delegué au skill reposcope-extract
    # Ici, nous supposons que l'artefact est produit
    if (-not (Test-Path $extractPath)) {
        Write-Output "[ERROR] Échec de l'étape EXTRACT"
        exit 1
    }
    $extractPath
}

# ÉTAPE 2 — SCORE
Write-Output "[reposcope-compare] ÉTAPE 2: SCORING"
$scoreOutput = & {
    $scorePath = "NEXUS/reposcope/score_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    if (-not (Test-Path $scorePath)) {
        Write-Output "[ERROR] Échec de l'étape SCORE"
        exit 2
    }
    $scorePath
}

# ÉTAPE 3 — PROPAGATE
Write-Output "[reposcope-compare] ÉTAPE 3: PROPAGATION"
$propagateOutput = & {
    $propagatePath = "NEXUS/reposcope/propagate_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    if (-not (Test-Path $propagatePath)) {
        Write-Output "[ERROR] Échec de l'étape PROPAGATE"
        exit 4
    }
    $propagatePath
}

# ÉTAPE 4 — ARTEFACT
Write-Output "[reposcope-compare] ÉTAPE 4: GÉNÉRATION ARTEFACT"
$artefactOutput = & {
    $artefactPath = "NEXUS/reposcope/reposcope_compare_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    if (-not (Test-Path $artefactPath)) {
        Write-Output "[ERROR] Échec de l'étape ARTEFACT"
        exit 5
    }
    $artefactPath
}

# ÉTAPE 5 — NOTIFICATION (FLUX/BRAIN/GITNOTE)
# Déjà gérée dans les étapes PROPAGATE et ARTEFACT via leurs effets de bord

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds
Write-Output "[reposcope-compare] Pipeline terminé en [${duration}s]"
Write-Output "[reposcope-compare] Artefact final: $artefactOutput"
```

### Étape 6 — Codes de sortie

| Code | Signification |
|---|---|
| 0 | Succès |
| 1 | Échec extraction |
| 2 | Échec scoring |
| 3 | Lock file actif (exécution concurrente) |
| 4 | Échec propagation |
| 5 | Échec génération artefact |

## Gestion des options (extensible)

```powershell
# Options futures (pas encore implémentées v1.0)
# --depth <shallow|full>
# --notify           # Force notification même si score bas
# --schedule <daily|weekly|monthly>  # Ajoute à la watch list KRONOS
# --output <path>    # Chemin de sortie personnalisé
# --dry-run          # Exécute sans écrire dans NEXUS/ARGUS
```

## Critères de succès

- [ ] `reposcope-compare <url>` exécute le pipeline complet
- [ ] Codes de sortie corrects selon l'étape d'échec
- [ ] Lock file empêche les exécutions concurrentes sur le même repo
- [ ] Artefact final produit dans NEXUS
- [ ] Effets de bord : événements FLUX, note BRAIN-FEED, note Gitnote, entrée ARGUS

## Skills liés

- **reposcope-extract** : étape 1 du pipeline
- **reposcope-score** : étape 2 du pipeline
- **reposcope-propagate** : étape 3 du pipeline
- **reposcope-artefact** : étape 4 du pipeline

## TODO v2.0

- Implémenter les options de ligne de commande
- Ajouter le reporting de progression détaillée
- Intégrer avec KRONOS pour le scheduling
- Ajouter la gestion de la watch list (`reposcope-watch add/list/remove`)
