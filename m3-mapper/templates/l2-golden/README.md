# Golden Template L2-PLATFORM

## Objectif
Ce template canonique définit le standard minimal pour tout dépôt de strate L2-PLATFORM.

## Composants

### 1. REPO.yaml.template
Contrat de base définissant :
- `layer: L2-PLATFORM` (obligatoire)
- `intentHash` unique
- Dépendance vers CTULU
- Métadonnées de gouvernance

### 2. ci.yml.template
Pipeline GitHub Actions minimal :
- Validation REPO.yaml
- Exécution des tests (si présents)
- Check bridge-schema (si bridges présents)

### 3. pre-commit.ps1.template
Hooks Git canoniques :
- Détection de secrets
- Contrôle taille fichiers
- Validation bridge-schema
- Validation REPO.yaml

## Propagation

```bash
# Test sur un dépôt (dry-run)
python propagate_template.py /path/to/repo --dry-run

# Propagation réelle
python propagate_template.py /path/to/repo
```

## Critères de conformité

Un dépôt L2 est considéré **INDUSTRIALIZED** si :
- ✅ REPO.yaml valide avec `layer: L2-PLATFORM`
- ✅ CI GitHub Actions présente
- ✅ Hooks pre-commit avec bridge-schema
- ✅ Dépendance CTULU déclarée
