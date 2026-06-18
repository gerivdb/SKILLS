# CAPTA Scene Layout — Modélisation de Scène

## Description

Modélisation de la scène pour systèmes câblés — ancrage câbles, position moteurs, zones de travail. Ce skill documente la structure spatiale des scènes CAPTA-4D.

## Quand l'utiliser

- Mentionne "scène", "layout", "ancrage", "position", "moteur", "workspace"
- Création d'un nouveau profil de scène (RigPosition)
- Configuration des points d'ancrage
- Définition des zones de travail

## Structure d'une scène

```yaml
# config/scene.yaml
name: "scene-4d-default"
anchors:
  - [0.0, 0.0, 6000.0]      # Ancrage 0: coin inférieur gauche
  - [10000.0, 0.0, 6000.0]   # Ancrage 1: coin inférieur droit
  - [10000.0, 10000.0, 6000.0] # Ancrage 2: coin supérieur droit
  - [0.0, 10000.0, 6000.0]   # Ancrage 3: coin supérieur gauche
workspace:
  x_min: 500
  x_max: 9500
  y_min: 500
  y_max: 9500
  z_min: 500
  z_max: 5500
tension_limits:
  t_min: 10.0
  t_max: 5000.0
named_positions:
  home: [5000.0, 5000.0, 3000.0]
  park: [2000.0, 2000.0, 4000.0]
```

## Convention de nommage

| Élément | Pattern | Exemple |
|---------|---------|---------|
| Ancrage | `anchor_N` | `anchor_0`, `anchor_1` |
| Position nommée | `snake_case` | `home`, `park`, `loading_zone` |
| Scène | `scene-<suffix>` | `scene-4d-default`, `scene-pitch1` |
| Profil | `<name>.yaml` | `default.yaml`, `pitch1.yaml` |

## Géométrie

- **Ancrages**: points 3D fixes (mm) — forment le polygone de support
- **Workspace**: volume de travail (mm) — boîte englobante
- **Câbles**: lignes entre ancrages et charge — longueur calculée par cinématique
- **Zones de sécurité**: sous-espaces du workspace — validation avant mouvement

## Procédures

### Créer une scène
```bash
capta-4d profile create my-scene
```

### Valider une position
```bash
capta-4d validate my-scene.yaml 5000 5000 3000
```

### Lister les positions nommées
```bash
capta-4d profile show my-scene.yaml
```

## Références

- Code: `gerivdb/CAPTA-4D/src/capta4d/core/profiles.py`
- Config: `gerivdb/CAPTA-4D/config/default.yaml`
- Tests: `gerivdb/CAPTA-4D/tests/test_orchestrator.py`
