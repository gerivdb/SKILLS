---
type: SKILL
version: "1.0.0"
intent_hash: 0xAGENT_MANAGER_API_SERVER_20260808
---

# Agent Manager API Server

## Objectif

Exposer l'API REST/CLI pour le pilotage fine-grained des sessions Agent Manager.

## Déclencheur

Lors de l'initialisation de l'Agent Manager V9.9.

## Règles

### 1. Démarrer le serveur HTTP

```powershell
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://localhost:18001/")
$listener.Start()
```

### 2. Routes disponibles

| Route | Méthode | Description |
|-------|---------|-------------|
| `/health` | GET | Statut du serveur |
| `/sessions` | GET | Liste des sessions actives |
| `/start` | POST | Démarrer une session |
| `/stop` | POST | Arrêter une session |
| `/pause` | POST | Mettre en pause |
| `/resume` | POST | Reprendre |
| `/switch-mode` | POST | Changer de mode |
| `/inject-context` | POST | Injecter du contexte |
| `/callback/{session_id}` | POST | Callback de session |

### 3. Gérer les sessions

```powershell
$sessions = @{}
function Start-Session {
    param($sessionId, $mode, $targetRepos)
    $sessions[$sessionId] = @{
        id = $sessionId
        mode = $mode
        target_repos = $targetRepos
        status = "running"
        started_at = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    }
}
```

### 4. Intégration WAL NEXUS

```powershell
# Logger chaque opération dans WAL
[API_START] session=<id>, mode=<mode>, repos=<n>
[API_STOP] session=<id>, reason=<reason>
[API_SWITCH] session=<id>, from=<old>, to=<new>
```

## Anti-patterns bloquants

- Port 18001 déjà occupé → BLOCKING
- Session inexistante → BLOCKING
- Mode invalide → BLOCKING

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENT-MANAGER-V99
- **IntentHash** : 0xAGENT_MANAGER_V99_20260808
- **Statut ADR** : proposed
