# M3 Skill — Code Auto-Fix (Self-Healing pour Patterns Code)
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xM3_SKILL_CODE_AUTO_FIX_20261123

## Définition
Orchestrateur d'auto-correction de patterns de code défectueux détectés dans les skills Python.
Détecte et corrige automatiquement les patterns anti-patterns connus :
- Double `await cdp_send` + `while True: await ws.recv()` → remplace par retour direct
- Paramètre `ws` manquant dans appels `evaluate_js` → ajoute `ws` en premier argument
- Double `await ws.recv()` → supprime le doublon
- Timeouts > 30s sans logging → ajoute logging

## Prérequis
- Python 3.10+
- Accès lecture/écriture aux skills dans `L4-TOOLS/SKILLS/`

## Patterns auto-corrigés

| Pattern détecté | Correction appliquée |
|-----------------|---------------------|
| `await cdp_send(...)` suivi de `while True: await ws.recv()` | Remplace par `resp = await cdp_send(...)` et retourne `resp` |
| `await ws.recv()` suivi de `await ws.recv()` | Supprime le doublon |
| `evaluate_js(expression, msg_id)` sans `ws` | Ajoute `ws` en premier argument: `evaluate_js(ws, expression, msg_id)` |
| `timeout` > 30000 sans logging adjacent | Ajoute `logger.warning(f"Timeout {timeout}ms")` avant |

## GESTES (séquence atomique)

### GESTE-1 — Scanner les skills Python
```
Trouver tous les .py dans L4-TOOLS/SKILLS/**/*.py
Exclure les fichiers de test et __pycache__
```

### GESTE-2 — Détecter patterns
Appliquer les regex patterns sur chaque fichier .py
Collecter les violations avec ligne et contexte

### GESTE-3 — Appliquer corrections
Pour chaque violation détectée :
1. Sauvegarder le fichier original (.bak)
2. Appliquer la transformation regex
3. Valider la syntaxe Python (ast.parse)
4. Si valide → garder, sinon restaurer .bak

### GESTE-4 — Valider
Exécuter `python -m py_compile` sur le fichier corrigé
Si succès → commiter les changements
Si échec → restaurer .bak, logger erreur

### GESTE-5 — Rapport
Sortie JSON :
```json
{
  "ok": true,
  "files_processed": N,
  "fixes_applied": [
    {"file": "path", "pattern": "pattern_name", "line": N, "action": "fixed|skipped|failed"}
  ]
}
```

## Règles d'or
- Toujours sauvegarder avant modification (.bak)
- Valider syntaxe Python après correction (ast.parse)
- Ne jamais modifier sans backup
- Logger chaque correction dans WAL
- Respecter la règle HOTL: un fichier par commit

## Preuve d'exécution
- Date/heure : 2026-11-23T22:50:00Z
- WAL: 0x243
- IntentHash: 0xM3_SKILL_CODE_AUTO_FIX_20261123

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Script principal | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skill-code-auto-fix\auto_fix.py` |
| Config patterns | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skill-code-auto-fix\patterns.json` |
| Tests | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skill-code-auto-fix\test_auto_fix.py` |

## Hash de ce skill
Horodatage: 2026-11-23T22:55:00Z | WAL: 0x243 | IntentHash: 0xM3_SKILL_CODE_AUTO_FIX_20261123