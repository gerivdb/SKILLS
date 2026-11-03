---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_PVIC_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/python-venv-isolation-checker/SKILL.md
---

# Skill - python-venv-isolation-checker

## Objectif

Empecher l'execution de commandes pip polluant l'environnement Python systeme global au lieu d'un environnement virtuel (venv) cible. Garantit l'isolation des dependances par projet sur l'hote Windows ENV2.

## Declencheur

- Commande pip invoquee sans environnement virtuel active.
- Installation dans le repertoire site-packages systeme global.
- Tentative de pip install --user sans venv.
- Risque de pollution de l'environnement Python systeme par des dependances de projet.

## Entrees

- Commande pip a executer (ex: pip install, pip uninstall, pip list).
- Chemin de l'environnement virtuel cible (ex: .venv, venv, env).
- Fichier requirements.txt ou pyproject.toml du projet.

## Sorties

- Avertissement si pip est utilise hors environnement virtuel.
- Blocage de la commande pip si aucun venv n'est detecte.
- Redirection vers l'environnement virtuel cible si present.
- Rapport d'action avec le chemin de l'interpreteur Python utilise.

## Regles Operationnelles

### 1. Verification de l'activation du venv
Avant toute commande pip, verifier qu'un environnement virtuel est active :
```powershell
$env:VIRTUAL_ENV
```
Si cette variable est absente, bloquer l'execution.

### 2. Verification du prefixe d'installation
Verifier que pip installera dans le repertoire du venv et non dans site-packages systeme :
```powershell
pip -V
# Verifier que le chemin pointe vers le venv, pas vers Python systeme
```

### 3. Interdiction de pip install --user sans venv
Rejeter toute commande pip install --user qui n'est pas precedee d'une activation de venv.

### 4. Redirection automatique
Si un dossier .venv ou venv existe dans le repertoire du projet, suggerer son activation avant de proceder :
```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Escalade
Si l'utilisateur insiste pour installer en systeme malgre l'avertissement, signaler l'action pour audit HITL.
