# M3 Skill — Debug Enforcer (Pre-commit Gate for Python Patterns)
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xM3_SKILL_DEBUG_ENFORCER_20261123

## Définition
Gate pre-commit qui scanne les fichiers Python modifiés pour détecter les patterns anti-patterns connus (double await ws.recv(), paramètre ws manquant, timeouts > 30s sans logging, double await cdp_send + while True: await ws.recv(), paramètre ws manquant dans appels de fonctions). Bloque le commit si patterns détectés.

## Prérequis
- Python 3.10+
- Git (pour récupérer les fichiers modifiés via `git diff --cached --name-only`)

## Patterns détectés (regex)

| Pattern | Description | Sévérité |
|---------|-------------|----------|
| `await\s+cdp_send\s*\([^)]*\)\s*.*\s*while\s+True:\s*await\s+ws\.recv\(\)` | Double attente cdp_send + while ws.recv | CRITIQUE |
| `await\s+ws\.recv\(\)\s*.*\s*await\s+ws\.recv\(\)` | Double await ws.recv | CRITIQUE |
| `async\s+def\s+\w+\s*\([^)]*\)\s*:(?!.*\bws\b)` | Fonction async sans paramètre ws (heuristique) | AVERTISSEMENT |
| `timeout\s*[=>]\s*(?:[3-9]\d|[1-9]\d{2,})` | Timeout > 30s sans logging | AVERTISSEMENT |
| `cdp_send\s*\([^)]*\)\s*.*\s*while\s+True:\s*await\s+ws\.recv\(\)` | Pattern cdp_send + while ws.recv | CRITIQUE |
| `async\s+def\s+\w+\s*\([^)]*(?:,\s*)?\)\s*:` | Fonction async sans ws dans signature (heuristique) | INFO |

## GESTES (séquence atomique)

### GESTE-1 — Récupérer fichiers modifiés
```powershell
git diff --cached --name-only -- "*.py"
```

### GESTE-2 — Scanner chaque fichier
Pour chaque fichier .py staged :
1. Lire le contenu
2. Appliquer les regex patterns
3. Collecter les violations avec ligne et contexte

### GESTE-3 — Décision
- Si violations CRITIQUE → bloquer commit (exit 1)
- Si violations AVERTISSEMENT → warning mais permettre commit
- Si violations INFO → log seulement

### GESTE-4 — Rapport
Sortie JSON structurée :
```json
{
  "ok": true|false,
  "files_scanned": N,
  "violations": [
    {"file": "path", "line": N, "pattern": "pattern_name", "severity": "CRITICAL|WARNING|INFO", "context": "code snippet"}
  ]
}
```

## Règles d'or
- Jamais de commit sans passage par ce gate
- Patterns mis à jour via ADR post-mortem
- Intégré dans session-boot-sequence (BOOT-0)

## Preuve d'exécution
- Date/heure : 2026-11-23T22:35:00Z
- WAL: 0x243
- IntentHash: 0xM3_SKILL_DEBUG_ENFORCER_20261123

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Script principal | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skill-debug-enforcer\debug_enforcer.py` |
| Hook pre-commit | `.git/hooks/pre-commit` (appelle debug_enforcer.py) |
| Config patterns | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skill-debug-enforcer\patterns.json` |

## Hash de ce skill
Horodatage: 2026-11-23T22:35:00Z | WAL: 0x243 | IntentHash: 0xM3_SKILL_DEBUG_ENFORCER_20261123