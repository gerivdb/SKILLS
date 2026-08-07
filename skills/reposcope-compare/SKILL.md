---
name: reposcope-compare
version: "1.0"
intent_hash: 0xSKILL_REPOSCOPE_COMPARE_20260615
---

# Skill: reposcope-compare

## Quand l'utiliser

- L'utilisateur veut executer le pipeline complet REPOSCOPE-COMPARE sur un repo externe
- ECOS-CLI `reposcope-compare <owner>/<repo>` est appele

**NE PAS utiliser** pour des analyses partielles (utiliser les skills individuels a la place).

## References

- **INTENT** : INTENT-041e (GOVERNANCE-HUB)
- **PRD** : PRD-REPOSCOPE-PIPELINE-2026-06-15
- **EPIC** : EPIC-REPOSCOPE-PIPELINE

## Pipeline orchestre

### Etape 1 - Valider l'entree

```powershell
param(
    [Parameter(Mandatory=$true)] [string] $RepoUrl
)

if ($RepoUrl -notmatch '^[\w-]+/[\w-]+$') {
    Write-Output "[ERROR] URL invalide. Format attendu: <owner>/<repo>"
    exit 1
}
```

### Etape 2 - Gestion du lock file (prevention des executions concurrentes)

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
        Write-Output "[ERROR] Un autre processus traite deja ce repo. Lock file: $lockPath"
        exit 3
    } else {
        # Lock perime (>24h), le supprimer
        Remove-Item $lockPath -Force
    }
}

# Creer le lock
New-Item -ItemType File -Path $lockPath -Value (Get-Date -Format "o") | Out-Null

try {
    # ... [pipeline] ...
} finally {
    # Toujours supprimer le lock a la fin
    if (Test-Path $lockPath) {
        Remove-Item $lockPath -Force
    }
}
```

### Etape 3 - Pipeline sequentiel

```powershell
Write-Output "[reposcope-compare] Demarrage pipeline pour $RepoUrl"
$startTime = Get-Date

# GATE-0 - Chargement SOT (cache dans competences)
Write-Output "[reposcope-compare] GATE-0: Chargement SOT..."
# Les skills individuels chargent leurs propres SOT avec cache

# ETAPE 1 - EXTRACT
Write-Output "[reposcope-compare] ETAPE 1: EXTRACTION"
$extractOutput = & {
    # Appel au skill reposcope-extract via le mecanisme Kilo
    # En pratique : cela serait fait via une invocation de skill ou un script wrapper
    # Pour ce skill, nous decrivons la logique
    $extractPath = "NEXUS/reposcope/extract_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    # Simuler l'appel : en realite, ce serait delegue au skill reposcope-extract
    # Ici, nous supposons que l'artefact est produit
    if (-not (Test-Path $extractPath)) {
        Write-Output "[ERROR] Echec de l'etape EXTRACT"
        exit 1
    }
    $extractPath
}

# ETAPE 2 - SCORE
Write-Output "[reposcope-compare] ETAPE 2: SCORING"
$scoreOutput = & {
    $scorePath = "NEXUS/reposcope/score_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    if (-not (Test-Path $scorePath)) {
        Write-Output "[ERROR] Echec de l'etape SCORE"
        exit 2
    }
    $scorePath
}

# ETAPE 3 - PROPAGATE
Write-Output "[reposcope-compare] ETAPE 3: PROPAGATION"
$propagateOutput = & {
    $propagatePath = "NEXUS/reposcope/propagate_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    if (-not (Test-Path $propagatePath)) {
        Write-Output "[ERROR] Echec de l'etape PROPAGATE"
        exit 4
    }
    $propagatePath
}

# ETAPE 4 - ARTEFACT
Write-Output "[reposcope-compare] ETAPE 4: GENERATION ARTEFACT"
$artefactOutput = & {
    $artefactPath = "NEXUS/reposcope/reposcope_compare_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
    if (-not (Test-Path $artefactPath)) {
        Write-Output "[ERROR] Echec de l'etape ARTEFACT"
        exit 5
    }
    $artefactPath
}

# ETAPE 5 - NOTIFICATION (FLUX/BRAIN/GITNOTE)
# Deja geree dans les etapes PROPAGATE et ARTEFACT via leurs effets de bord

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds
Write-Output "[reposcope-compare] Pipeline termine en [${duration}s]"
Write-Output "[reposcope-compare] Artefact final: $artefactOutput"
```

### Etape 6 - Codes de sortie

| Code | Signification |
|---|---|
| 0 | Succes |
| 1 | Echec extraction |
| 2 | Echec scoring |
| 3 | Lock file actif (execution concurrente) |
| 4 | Echec propagation |
| 5 | Echec generation artefact |

## Gestion des options (extensible)

```powershell
# Options futures (pas encore implementees v1.0)
# --depth <shallow|full>
# --notify           # Force notification meme si score bas
# --schedule <daily|weekly|monthly>  # Ajoute a la watch list KRONOS
# --output <path>    # Chemin de sortie personnalise
# --dry-run          # Execute sans ecrire dans NEXUS/ARGUS
```

## Criteres de succes

- [ ] `reposcope-compare <url>` execute le pipeline complet
- [ ] Codes de sortie corrects selon l'etape d'echec
- [ ] Lock file empeche les executions concurrentes sur le meme repo
- [ ] Artefact final produit dans NEXUS
- [ ] Effets de bord : evenements FLUX, note BRAIN-FEED, note Gitnote, entree ARGUS

## Skills lies

- **reposcope-extract** : etape 1 du pipeline
- **reposcope-score** : etape 2 du pipeline
- **reposcope-propagate** : etape 3 du pipeline
- **reposcope-artefact** : etape 4 du pipeline

## TODO v2.0

- Implementer les options de ligne de commande
- Ajouter le reporting de progression detaillee
- Integrer avec KRONOS pour le scheduling
- Ajouter la gestion de la watch list (`reposcope-watch add/list/remove`)
