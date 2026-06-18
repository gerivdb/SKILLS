# CAPTA-4D Core — Domaine Câble/Kinématique/4D

## Description

Moteur de positionnement 4D pour systèmes câblés — cinématique, contraintes, sécurité, orchestration. Ce skill documente le vocabulaire, les patterns, et les procédures du domaine CAPTA-4D.

## Quand l'utiliser

- L'utilisateur mentionne "CAPTA", "câble", "kinématique", "positionnement 4D", "scène", "ancrage"
- Création/modification de modèles dans `src/capta4d/core/`
- Validation de scènes cinématiques
- Calcul de longueurs/tensions de câbles

## Vocabulaire domaine

| Terme | Définition |
|-------|-----------|
| **Ancrage** | Point fixe d'attache d'un câble (3D: x,y,z) |
| **Câble** | Lien élastique entre un ancrage et une charge — longueur, tension, raideur |
| **Scène** | Configuration complète: ancrages + câbles + contraintes + sécurité |
| **Kinematics** | Calcul des longueurs de câble depuis positions 3D (CableKinematics) |
| **Contraintes** | Limites physiques: tension min/max, zones de sécurité (SceneConstraints) |
| **Sécurité** | Surveillance temps réel des dépassements (SafetyGuard) |
| **Profil** | Configuration nommée d'une scène (RigProfile) |
| **Orchestrateur** | Séquenceur de solve + validate + report (Orchestrator) |

## Fichiers clés

```
src/capta4d/
├── core/
│   ├── kinematics.py    # CableKinematics — solve(), jacobian()
│   ├── constraints.py   # SceneConstraints — validate(), zones
│   ├── profiles.py      # RigProfile — load_profile(), save_profile()
│   ├── safety.py        # SafetyGuard — check(), thresholds
│   └── orchestrator.py  # Orchestrator — solve(), reset()
├── cli/
│   └── main.py          # CLI Click — validate, solve, profile
└── config/
    └── default.yaml     # Configuration par défaut
```

## Procédures

### Validation de scène
```bash
capta-4d validate <profile.yaml> <x> <y> <z>
```

### Résolution cinématique
```bash
capta-4d solve <profile.yaml> <x> <y> <z>
```

### Gestion des profils
```bash
capta-4d profile show <profile.yaml>
capta-4d profile create <name>
```

## Invariants

- Toute scène doit avoir ≥ 4 ancrages (tétraèdre minimal)
- Les tensions doivent rester dans [t_min, t_max] du profil
- La workspace doit contenir la position cible
- Le safety monitor bloque toute opération si P(harm) > seuil

## Références

- Code source: `gerivdb/CAPTA-4D/src/capta4d/`
- Tests: `gerivdb/CAPTA-4D/tests/`
- Config: `gerivdb/CAPTA-4D/config/default.yaml`
