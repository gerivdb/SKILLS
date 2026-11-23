# Skill: skill-ecosystem-auditor

## Description
Audite l'écosystème complet des skills L4 : détecte les doublons, les skills orphelins (sans fichier SKILL.md), les dépendances circulaires, les chemins de registre non cohérents, et les conflits de noms. C'est le gardien de l'intégrité du registre de skills.

## Déclencheurs
- Mentions : "audit skills", "écosystème skills", "vérifier skills", "drift skills", "skills orphelins"

## Invariants vérifiés
- Chaque dossier dans `SKILLS/` contient un `SKILL.md`
- Aucun doublon de nom de skill dans le registre
- Chaque skill référencé dans `REGISTRY.yaml` existe physiquement
- Chaque skill physique a une entrée dans `REGISTRY.yaml`
- Pas de dépendance circulaire entre skills (via `dependencies`)

## Flux d'exécution
1. Scanner `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\`
2. Comparer avec `REGISTRY.yaml`
3. Produire un rapport : skills orphelins, skills manquants, doublons, conflits
4. Écrire un WAL d'audit si `SKILL-REGISTRY` citoyen est actif

## Liens
- Dépend de : aucun
- Dépendants : `skill-version-bumper`, `skill-pruner-retire`
- Citoyen cible : `SKILL-REGISTRY` (L3-CITIZENS)

## Statut
- Version : 1.0.0
- Statut : active
- Type : domain
- Autopoïèse : générateur de métadonnées pour le registre des skills