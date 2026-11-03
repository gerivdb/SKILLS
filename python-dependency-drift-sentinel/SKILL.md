---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_PDDS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/python-dependency-drift-sentinel/SKILL.md
---

# Skill - python-dependency-drift-sentinel

## Objectif

Détecter, isoler et corriger les dérives silencieuses de dépendances transitives dans l'environnement Python d'exécution (notamment les désynchronisations de signatures entre sous-bibliothèques mises à jour et frameworks parents, telles que FastAPI vs Starlette ou Pydantic vs Pydantic-core).

## Déclencheurs

- Apparition d'erreurs `TypeError: ... got an unexpected keyword argument` localisées dans un appel interne à `super().__init__()` au sein de `site-packages`.
- Crash immédiat à l'instanciation de routeurs (`APIRouter`) ou de modèles de données, alors que le code source utilisateur ne contient pas le paramètre incriminé.
- Après l'installation ou la mise à jour d'un package tiers (ex: extension MCP, Jupyter, client HTTP).

## Entrées

- Arborescence du projet cible (accès au `pyproject.toml` ou `requirements.txt`).
- Environnement Python courant (`sys.executable`, packages `site-packages`).

## Sorties

- Rapport d'incohérence binaire des packages (`pip check`).
- Alignement contractuel de la version parente avec sa sous-bibliothèque mise à jour.
- Entrée de validation d'import sans effet de bord.

## Règles Opérationnelles

### 1. Interdiction de modifier le code métier prématurément
Ne jamais altérer le code source applicatif (ex: enlever un décorateur, contourner un appel de routeur) lorsqu'un `TypeError` interne à une bibliothèque tierce survient.

### 2. Audit de rupture de signature (Traceback Inspection)
Lorsque l'exception remonte `super().__init__(..., param=val)`, identifier la classe mère et le package d'origine dans `site-packages`.
Exemple canonique :
- `fastapi/routing.py` appelant `starlette.routing.Router.__init__(..., on_startup=...)`.
- Si Starlette >= 1.0 a supprimé `on_startup`, c'est FastAPI qui est obsolète par rapport à Starlette.

### 3. Vérification de l'intégrité de l'environnement
Exécuter systématiquement :
```powershell
pip check
```
Et relever les couples de versions en conflit :
```powershell
python -c "import pkg_parent, pkg_child; print(pkg_parent.__name__, pkg_parent.__version__, '|', pkg_child.__name__, pkg_child.__version__)"
```

### 4. Réconciliation contractuelle
1. Consulter le fichier de dépendances du projet (`pyproject.toml`).
2. Vérifier si la borne supérieure autorise la mise à jour (ex: `fastapi>=0.109.0`).
3. Si autorisé, mettre à niveau le package parent pour rétablir la compatibilité :
   ```powershell
   pip install --upgrade <package_parent>
   ```
4. Valider par un test d'import statique unitaire avant toute relance de service.

