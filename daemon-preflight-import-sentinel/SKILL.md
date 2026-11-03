---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_DPIS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/daemon-preflight-import-sentinel/SKILL.md
---

# Skill - daemon-preflight-import-sentinel

## Objectif

Interdire formellement tout démarrage de serveur ASGI/WSGI (Uvicorn, Gunicorn), démon en tâche de fond ou écoute sur un port réseau tant que le code source, les dépendances et les routeurs n'ont pas passé avec succès un test d'import statique en mémoire unitaire et sans effet de bord.

## Déclencheurs

- Avant toute exécution de commande de lancement de serveur : `gateway-manager start`, `uvicorn`, `python -m <app>.server`.
- Après toute modification apportée aux routeurs, middlewares ou fichiers d'initialisation (`server.py`, `lifespan`, `cli.py`).
- Suite à un signalement d'erreur au démarrage ou un crash immédiat post-bind.

## Entrées

- Chemin racine du projet hôte.
- Entrypoint officiel de l'application (ex: `gateway_manager.server:app`).

## Sorties

- Code retour 0 sur l'import statique en mémoire.
- Détection immédiate de toute exception bloquante (`SyntaxError`, `ImportError`, `TypeError`) sans pollution réseau.
- Autorisation formelle de démarrage du démon.

## Règles Opérationnelles

### 1. Règle absolue du "Zero-Daemon Before Zero-Error"
Il est strictement interdit de démarrer un démon ou de lancer un processus en tâche de fond pour « voir si ça démarre ». Le démarrage d'un serveur ne doit être exécuté QUE lorsque l'import statique a réussi à 100 %.

### 2. Purge préalable du cache bytecode
Avant de tester l'import, purger les fichiers `.pyc` et dossiers `__pycache__` pour éviter tout faux positif issu d'un bytecode obsolète :
```powershell
Get-ChildItem -Path "src" -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
Get-ChildItem -Path "src" -Include *.pyc -Recurse -Force | Remove-Item -Force
```

### 3. Test d'import statique unitaire
Exécuter l'import direct de l'application sans instancier le serveur web :
```powershell
$env:PYTHONPATH = "src"
python -c "from <module>.server import app; print('PREFLIGHT_IMPORT_OK')"
```

### 4. Protocole d'escalade en cas d'échec
- Si échec sur `super().__init__` ou incohérence de paramètres -> Router immédiatement vers `python-dependency-drift-sentinel`.
- Si échec sur `ImportError (unknown location)` ou symbole absent -> Router vers `python-package-integrity-prober`.
- Si échec de syntaxe -> Corriger localement avant toute autre tentative.

### 5. Démarrage sécurisé
Ce n'est qu'après l'affichage de `PREFLIGHT_IMPORT_OK` que la commande de démarrage réseau (ex: `gateway-manager start --host 0.0.0.0 --port 9000`) est autorisée.

