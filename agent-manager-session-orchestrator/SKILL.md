---
type: SKILL
version: "1.0.0"
intent_hash: 0xAGENT_MANAGER_SESSION_ORCHESTRATOR_20260808
---

# Agent Manager Session Orchestrator

## Objectif

Orchestrer les sessions Kilocode : callback watching, auto-dispatch, mission queue, WAL NEXUS.

## Déclencheur

Au démarrage de l'Agent Manager V9.9 et après chaque événement de session.

## Règles

### 1. Surveiller les callbacks

```powershell
# Surveiller le répertoire des callbacks
$callbacksDir = ".kilo/session_callbacks"
$watcher = New-Object System.IO.FileSystemWatcher $callbacksDir, "*.json"
$watcher.EnableRaisingEvents = $true
```

### 2. Détecter les sessions libres

```powershell
# Parcourir les callbacks pour trouver sessions completed/failed
$callbacks = Get-ChildItem $callbacksDir -Filter "*.json"
foreach ($cb in $callbacks) {
    $data = Get-Content $cb.FullName -Raw | ConvertFrom-Json
    if ($data.status -eq "completed" -or $data.status -eq "failed") {
        # Session libre = à réassigner
        $freeSessions += $data
    }
}
```

### 3. Réassigner aux missions pending

```powershell
# Lire mission_queue.yaml et trouver première mission pending
$queue = Get-Content ".kilo/mission_queue.yaml" -Raw
$pending = $queue | Select-String "status: pending" | Select-Object -First 1
if ($pending) {
    # Réassigner la session libre à cette mission
    Update-MissionStatus -MissionId $pending.id -Status "assigned"
}
```

### 4. Logger dans WAL NEXUS

```
[AUTO_DISPATCH] session=<session_id>, mission=<mission_id>, timestamp=<iso>
```

## Anti-patterns bloquants

- Deux sessions sur même mission → BLOCKING
- Réassigner sans vérifier RAM budget → BLOCKING
- Ignorer callback failed → BLOCKING

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENT-MANAGER-V99
- **IntentHash** : 0xAGENT_MANAGER_V99_20260808
- **Statut ADR** : proposed
