---
name: kiva-pipeline
description: "KIVA-CLI pipelines, local CI, preflight, GitHub Actions migration. Use when user mentions 'KIVA', 'pipeline', 'CI locale', 'preflight'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritIsolate
---
# KIVA Pipeline

## Domaine et périmètre

Ce skill couvre le pipeline CI local KIVA-CLI et les adaptations matérielles HP Z600.

## Méthodologie

### Phase 1 : Diagnostic matériel
- Vérifier la compatibilité CPU (Xeon E5620, pas d'AVX)
- Vérifier l'état du GPU (Quadro 4000 Fermi, souvent en erreur)
- Vérifier la RAM disponible (< 8 GB pour les applis légères)

### Phase 2 : Configuration du pipeline
- Activer KIVA-CLI avec la commande `kiva init --no-avx`
- Configurer les tâches planifiées Windows (schtasks) pour la CI locale
- Désactiver les workflows GitHub Actions qui nécessitent un GPU

### Phase 3 : Exécution et validation
- Lancer un preflight avec `kiva preflight --target all`
- Analyser les logs, corriger les erreurs de compilation Zig (CodeDB-E5620)
- Valider la conformité NEXUS via `kiva validate`

## Règles de décision
- **Règle 1** : Toujours privilégier le CPU sur GPU Fermi (trop instable)
- **Règle 2** : Zig sans AVX = utiliser CodeDB-E5620 ou LYCOS
- **Règle 3** : KIVA-CLI remplace GitHub Actions pour la CI locale

## Format de sortie
```markdown
## Diagnostic pipeline
- État KIVA : ...
- Dernier run : ...
- Anomalies : ...

## Actions recommandées
1. ...
2. ...