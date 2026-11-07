---
type: SKILL
version: "1.0.0"
intent_hash: 0xAGENT_MANAGER_MODE_ROUTER_20260808
---

# Agent Manager Mode Router

## Objectif

Router les missions vers le mode Agent Manager optimal et permettre le switching à chaud.

## Déclencheur

Avant chaque assignation de mission et lors d'un switch de mode demandé.

## Règles

### 1. Sélectionner le mode selon la mission

```powershell
$modes = @{
    "code-reviewer"    = @("review","PR","pull request","code smell","analyse")
    "code-simplifier"  = @("refactor","simplify","clean","tech debt","duplication")
    "test-engineer"    = @("test","pytest","jest","coverage","TDD","BDD")
    "docs-specialist"  = @("docs","documentation","readme","markdown","narrative")
    "code-skeptic"     = @("security","audit","perf","skeptic","critique","vuln")
    "frontend-specialist" = @("frontend","UI","UX","component","style","accessibility")
    "architect"        = @("architect","design","pattern","ADR","schema","topology")
    "data"             = @("data","SQL","pipeline","analytics","dbt","warehouse")
    "dev-engine"       = @("dev-engine","RAI","KEEL","META-LOOP","auto-dev","citizen")
}
```

### 2. Calculer le score par mode

```powershell
$bestMode = "architect"
$bestScore = 0
foreach ($mode in $modes.Keys) {
    $score = 0
    foreach ($keyword in $mission.Keywords) {
        if ($modes[$mode] -contains $keyword) { $score += 3 }
    }
    if ($score -gt $bestScore) {
        $bestScore = $score
        $bestMode = $mode
    }
}
```

### 3. Switching à chaud

```powershell
# Vérifier que la session existe et est active
$session = Get-SessionState -SessionId $sessionId
if ($session.status -ne "running") {
    throw "Session must be running for hot-switch"
}

# Injecter le nouveau mode via contexte partagé
Inject-Context -SessionId $sessionId -Mode $newMode
```

## Anti-patterns bloquants

- Switch sur session inactive → BLOCKING
- Mode inexistant → BLOCKING
- Score nul sans mode par défaut → BLOCKING

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENT-MANAGER-V99
- **IntentHash** : 0xAGENT_MANAGER_V99_20260808
- **Statut ADR** : proposed
