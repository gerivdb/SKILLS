---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_PPIP_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/python-package-integrity-prober/SKILL.md
---

# Skill - python-package-integrity-prober

## Objectif

Diagnostiquer et réparer la corruption physique des packages Python installés dans l'environnement local (disparition de fichiers `__init__.py`, transformation silencieuse en *namespace package* vide, répertoires orphelins résiduels de désinstallation `~*`).

## Déclencheurs

- `ImportError: cannot import name 'X' from 'Y' (unknown location)`.
- Détection d'un package dont `getattr(module, '__file__', None)` vaut `None` alors qu'il devrait s'agir d'un module physique complet.
- Présence d'avertissements pip récurrents : `WARNING: Ignoring invalid distribution ~...`.

## Entrées

- Chemin vers le répertoire `site-packages` de l'interpréteur Python actif.
- Nom du package incriminé.

## Sorties

- Purge des répertoires orphelins corrompus (`~*`).
- Restauration de l'intégrité structurelle du package via réinstallation non-récursive.
- Validation de l'import physique du symbole exporté.

## Règles Opérationnelles

### 1. Nettoyage des dossiers résiduels de pip
Supprimer les résidus d'installations ou désinstallations interrompues qui polluent le résolveur de distributions :
```powershell
Get-ChildItem -Path "$((python -c 'import site; print(site.getsitepackages()[0])'))" -Filter "~*" | Remove-Item -Recurse -Force
```

### 2. Contrôle de l'emplacement et du type de package
Vérifier si le package est chargé en tant que namespace package ou module standard :
```powershell
python -c "import <package>; print('File:', getattr(<package>, '__file__', None)); print('Path:', getattr(<package>, '__path__', None))"
```
Si `File: None` et que le dossier du package sur le disque ne contient pas de fichier `__init__.py`, le package est corrompu ou incomplet.

### 3. Réinstallation ciblée et sans effet de bord
Ne pas exécuter un `pip install` massif qui risquerait de casser d'autres dépendances. Privilégier une réinstallation forcée sans toucher aux dépendances enfants (`--no-deps`) :
```powershell
pip install --force-reinstall --no-deps <package_nom>
```

### 4. Validation post-réparation
Vérifier que le symbole critique s'importe désormais avec son chemin de fichier réel :
```powershell
python -c "from <package> import <symbole>; print('INTEGRITY_OK')"
```

