# Comment les Skills fonctionnent dans ce Space

## Principe

Les skills dans ce Space ne sont pas des fonctions invoquées dynamiquement. Ils servent de **cadre de gouvernance opérationnel** : règles obligatoires, déclencheurs comportementaux et références documentaires.

L'assistant applique les règles directement depuis le prompt et consulte les fichiers sources pour le détail. Il n'y a pas de mécanisme `load_skill()` public documenté pour Perplexity SaaS — les skills sont portés par les instructions du Space et la knowledge base.

## Architecture en 3 couches

### Couche 1 — Règles obligatoires (toujours actives)

Les règles de conformité NEXUS, structure des dépôts, ADR, Git et ontologie sont actives en permanence. Elles ne dépendent d'aucun déclencheur — elles s'appliquent à toute interaction dans le Space.

Exemples :
- EPIC > 10 Ko → externaliser (spécification technique, pas un plan)
- Branches main/master protégées → jamais de push direct
- Taguer chaque dépôt/fichier : [CONFORME_NEXUS] | [À_VALIDER_NEXUS] | [HORS_NEXUS]

### Couche 2 — Déclencheurs (mot-clé → action)

Quand l'utilisateur mentionne certains mots-clés, l'assistant applique le comportement associé etConsulte la référence documentaire pour le détail.

Exemples :
- "NEXUS", "gouvernance", "φ-CPS" → valider conformité, émettre tag → Réf: nexus-core.md
- "ADR", "MADR" → créer/valider ADR, vérifier f-CPS → Réf: adr-manager.md
- "audit structure", "DDD" → scanner dépôt, rapporter violations → Réf: nexus-auditor.md

### Couche 3 — Références documentaires (consultatif)

Les 119 skills déclarés dans `REGISTRY.yaml` sont disponibles dans la knowledge base du Space et dans le repo `gerivdb/SKILLS/perplexity/skills/<nom>.md`. Ils apportent le détail des instructions, règles et formats quand la Couche 2 renvoie à la liste complète.

**État du registre (au 2026-11-09) :**
- 234 dossiers de skills dans `L4-TOOLS/SKILLS/`
- 187 dossiers contenant un `SKILL.md`
- 119 entrées dans `REGISTRY.yaml`
- 5 nouveaux skills de gouvernance méta ajoutés (voir ci-dessous)

### Skills de gouvernance méta (ajoutés le 2026-11-09)

| Skill | Rôle |
|-------|------|
| `skill-ecosystem-auditor` | Audite l'écosystème des skills L4 : détecte doublons, orphelins, dépendances circulaires, chemins de registre non cohérents |
| `skill-version-bumper` | Incrémente automatiquement les numéros de version V-4D dans SKILL.md et REGISTRY.yaml lors de modification d'un skill |
| `skill-dependency-healer` | Détecte et résout les dépendances manquantes ou circulaires entre skills L4 |
| `skill-template-evolver` | Fait évoluer le template canonique SKILL.md lorsqu'une nouvelle propriété est ajoutée à un skill existant |
| `skill-deployer` | Déploie un skill d'un dépôt source vers un dépôt cible (strate L* uniquement), avec sauvegarde WAL et vérification skill-linter-sentinel |

## Fichiers de référence

| Fichier | Rôle |
|---|---|
| `instructions_space_final.md` | Instructions complètes du Space (ce fichier) |
| `governance_prompt_v2.md` | Bloc gouvernance 3 couches (resserré) |
| `perplexity/skills/<nom>.md` | Détail de chaque skill |
| `perplexity/build/Skills_v3.zip` | ZIP importé dans la knowledge base |
| `perplexity/scripts/generate-skills.ps1` | Script de régénération du ZIP |
| `PROOF-CONTRACT.md` | Contrat de preuve GERIVDB : 14 principes de preuve et de gouvernance |


## Flux d'exécution

```
Utilisateur mentionne "NEXUS governance"
  → Couche 2: déclencheur "NEXUS","gouvernance","φ-CPS"
  → Action: valider conformité, émettre tag
  → Référence: nexus-core.md dans la knowledge base
  → Couche 1: règles globales appliquées (tagging, seuil φ-CPS...)
  → Réponse conform输出 avec verdict NEXUS
```

## Ajout ou modification d'un skill

Pour ajouter un nouveau skill ou modifier un skill existant :

1. Créer ou modifier le fichier `.md` dans `perplexity/skills/`
2. Mettre à jour les déclencheurs dans la Couche 2 du prompt si nécessaire
3. Régénérer le ZIP : `.\perplexity\scripts\generate-skills.ps1`
4. Ré-importer le ZIP dans la knowledge base du Space
5. Mettre à jour la liste des 119 skills dans la Couche 3

## Limitations connues

- Pas de `load_skill()` publique documentée pour Perplexity SaaS
- Les skills sont consultatifs (pas exécutables comme des fonctions)
- Le comportement dépend du contenu présent dans le prompt et la knowledge base
- Mettre à jour les règles Critiques dans les instructions du Space, pas seulement dans les fichiers source