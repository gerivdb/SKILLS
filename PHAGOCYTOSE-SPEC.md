# Protocole de phagocytose profonde — ENV2

**Version** : 1.0.0  
**IntentHash** : 0xPHAGOCYTOSE-SPEC_20261123  
**Dépôt** : `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\`  
**Statut** : accepted  
**Phase** : 4 (T031 à T040)

---

## 1. Définition

La phagocytose profonde désigne l'assimilation active, critique et structurée d'une source externe (dépôt GitHub, documentation, transcript de session, trace d'exécution, script isolé) pour en extraire des primitives réutilisables, plutôt qu'un simple survol ou un copier-coller passif.

Elle se déroule en 5 étapes obligatoires :

1. **Capture** — collecte fidèle et horodatée de la source brute
2. **Déconstruction** — tri anti-bruit, séparation faits vérifiés / hypothèses / dépendances
3. **Normalisation** — traduction au format canonique (SKILL.md, règles, chemins explicites, horodatage UTC)
4. **Validation** — test sur cas concret, contrôle absence de doublon, enregistrement preuve (EVIDENCE.md)
5. **Indexation** — inscription dans `skills-index.json` avec déclencheurs fiables pour réutilisation inter-shards

---

## 2. Déclencheurs de phagocytose (T032)

Un processus de phagocytose est déclenché par l'un des événements suivants :

| Déclencheur | Type | Description |
|-------------|------|-------------|
| `résolution-bug-non-trivial` | Manuel ou automatique | Un bug complexe a été résolu dans un shard, la procédure doit être conservée |
| `nouveau-script-valide` | Automatique | Un script a été testé avec succès (code de retour 0) et mérite d'être généralisé |
| `analyse-depot-externe` | Manuel | Un dépôt GitHub ou une documentation externe a été analysé et contient des patterns réutilisables |
| `derive-entre-shards` | Automatique | Une divergence de comportement est détectée entre deux shards sur une même tâche |
| `fin-de-tache-reutilisable` | Manuel | À la fin d'une tâche ayant produit un script ou une méthode réutilisable, l'opérateur décide de la phagocyter |
| `script-orphelin-decouvert` | Automatique | Un script trouvé sur disque sans documentation associée est candidat à phagocytose |

---

## 3. Étape 1 — Capture fidèle (T033)

### Objectif
Collecter la source brute complète, sans résumé prématuré, avec horodatage UTC et hash SHA-256 d'origine.

### Livrable
Un fichier d'archive de capture dans `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\captures\<nom-source>-<YYYYMMDDTHHmmssZ>.capture` contenant :
- Le contenu brut de la source (transcript, script, extrait de dépôt)
- L'URL ou le chemin de la source
- L'horodatage UTC de capture
- Le hash SHA-256 du contenu brut

### Règle
Aucun résumé n'est autorisé à cette étape. La capture doit être intégrale.

---

## 4. Étape 2 — Déconstruction et tri anti-bruit (T034)

### Objectif
Séparer explicitement :
- **Faits vérifiés** : ce qui a été testé, exécuté, confirmé sur ENV2
- **Hypothèses** : ce qui est supposé mais non vérifié
- **Dépendances non adaptées à ENV2** : bibliothèques, outils, versions incompatibles avec l'environnement Z600 (pas d'AVX2, RAM limitée, etc.)
- **Étapes reproductibles** : la séquence d'actions pouvant être rejouée sur un autre shard

### Livrable
Un fichier `deconstruction.json` dans le dossier de phagocytose avec les quatre sections ci-dessus.

---

## 5. Étape 3 — Normalisation (T035)

### Objectif
Traduire le résultat de la déconstruction au format canonique :
- Un fichier `SKILL.md` suivant `SPEC-SKILL-FORMAT.md` (frontmatter YAML, sections obligatoires, `anti_triggers`, `weight`, `hash_sha256_evidence`)
- Les fichiers associés sous `scripts/`, `references/`, `assets/`
- Des chemins absolus explicites (règle `explicit-path-compliance`)

### Livrable
Un dossier compétence dans `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\reviews\skill-drafts\<nom-du-skill>/` avec `SKILL.md`, `EVIDENCE.md` (vide, en attente de première utilisation), `HISTORY.md`.

---

## 6. Étape 4 — Validation & garde-fou (T036)

### Objectif
Tester le skill sur un cas concret, contrôler l'absence de doublon, et enregistrer la preuve.

### Contrôles obligatoires
1. **Validation syntaxique** : le SKILL.md passe `validate-skill.ps1` avec 0 erreur bloquante
2. **Test d'exécution** : les entrypoints du skill sont testés sur ENV2 (code de retour 0)
3. **Anti-doublon** : l'intent_hash n'est pas déjà présent dans `skills-index.json`
4. **Preuve fraîche** : le hash SHA-256 est recalculé sur le fichier actuel sur disque, pas copié d'un rapport précédent

### Livrable
Le skill passe en statut `candidat-validé` et est prêt pour promotion via `validate-skill.ps1 -AutoPromote` ou `-BaseSkill`.

---

## 7. Étape 5 — Indexation & réactivation (T037)

### Objectif
Inscrire le skill dans `skills-index.json` avec des déclencheurs fiables pour qu'il soit découvrable et activable depuis n'importe quel shard.

### Livrable
- `skills-index.json` régénéré via `index-skills.ps1`
- Le skill apparaît avec ses `triggers` pondérés et ses `anti_triggers`
- Le protocole de rappel inter-shards est fonctionnel : avant toute tâche, l'agent consulte l'index et active le(s) skill(s) pertinent(s)

---

## 8. Détection des dépendances non adaptées à ENV2 (T038)

### Contexte
ENV2 tourne sur une workstation HP Z600 (2× Xeon E5620, 16 threads, 24 Go DDR3 ECC, pas d'AVX2). Certaines bibliothèques ou outils nécessitent AVX2, AVX-512, ou une grande quantité de RAM.

### Règle
Tout skill phagocyté doit déclarer ses dépendances dans `prerequisites` et être testé sur ENV2 avant promotion. Une dépendance nécessitant AVX2 ou > 8 Go de RAM doit être signalée comme `non-adapte-ENV2` dans le frontmatter.

---

## 9. Archivage des sources phagocytées (T039)

### Objectif
Conserver la trace de la source brute phagocytée pour traçabilité et réexamen ultérieur.

### Emplacement
`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\archives\<nom-source>-<YYYYMMDDTHHmmssZ>/`

### Contenu
- Le fichier de capture brut (étape 1)
- Le fichier de déconstruction (étape 2)
- Une copie du SKILL.md final (étape 3-5)
- Le hash SHA-256 de chaque fichier

---

## 10. Test de phagocytose sur un cas concret (T040)

### Procédure
1. Choisir une source réelle (transcript de shard, script, dépôt externe)
2. Exécuter les 5 étapes via `phagocytose.ps1`
3. Vérifier que le skill résultant passe `validate-skill.ps1`
4. Vérifier que le skill est indexé dans `skills-index.json`
5. Vérifier que le skill peut être activé depuis un autre shard via ses `triggers`

---

## 11. Scripts associés

| Script | Tâche | Chemin |
|--------|-------|--------|
| `phagocytose.ps1` | T033 à T037 | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\phagocytose.ps1` |
| `phagocytose-detect-deps.ps1` | T038 | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\phagocytose-detect-deps.ps1` |

---

**Màj requise si** : modification du protocole des 5 étapes, ajout de déclencheurs, ou évolution du format de déconstruction.