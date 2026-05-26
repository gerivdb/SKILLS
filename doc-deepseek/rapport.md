## Récapitulatif — Génération de skills Perplexity & script PS1

### 1. Contexte de la mission

La demande initiale : produire un script PowerShell (`generate-53-skills-final.ps1`) générant un ZIP de **53 skills** pour Perplexity, respectant le **format canonique enrichi** (frontmatter YAML + corps Markdown). Ces skills couvrent l’écosystème `gerivdb` (NEXUS, Triade, PLIX, Z600, etc.).

Le script a été fourni, exécuté, et les fichiers .md téléversés un par un. Très vite, **43 fichiers sur 53 ont été rejetés** par Perplexity, et après analyse, la majorité contient un **contenu générique non actionnable**.

---

### 2. Ce qui fait un skill Perplexity **valide syntaxiquement**

#### Structure obligatoire

```yaml
---
name: <nom_unique>
description: "<description complète, avec mots-clés déclencheurs>"
---
|
# Titre

Corps en Markdown...
```

- Le frontmatter est un document YAML entre deux `---`.
- **Le `|` juste après le second `---` est crucial** : c’est l’indicateur de *bloc littéral* YAML. Sans lui, tout le corps est interprété comme une chaîne YAML, et la présence de `:`, `"`, `#`, etc. provoque une erreur de parsing.
- La première ligne après le frontmatter doit être un titre de niveau 1 (`#`).

#### Erreur principale de notre premier script

Dans `Write-CanonSkill`, nous faisions :

```powershell
$yaml = @"
---
name: $Name
description: "$DescriptionFull"
---

# $Title

$Body
"@
```

Il manquait le `|` sur la ligne qui suit le second `---`. Résultat : le Markdown n’était pas protégé, et les fichiers échouaient au téléversement.

**Correction** : ajouter `|` après le `---` final.

```powershell
$yaml = @"
---
name: $Name
description: "$DescriptionFull"
---
|
# $Title

$Body
"@
```

> C’est l’unique raison pour laquelle **43 fichiers sur 53** ont été rejetés.

---

### 3. Ce qui fait un skill **utile et actionnable**

Un skill Perplexity n’est pas un simple texte statique. Il doit guider le modèle pour répondre de manière **spécifique, outillée et contextuelle** à une catégorie de demandes.

#### a) Contenu **spécifique au domaine**

Le piège : utiliser un corps générique du type « Ce skill couvre les opérations et analyses relatives à son domaine… ». C’est exactement ce que notre script a injecté pour **32 skills**, via `$body_standard`. Ce template ne donne aucune information utile, aucun exemple concret, aucune règle métier. Le modèle ne peut rien en faire.

**À la place**, chaque skill doit contenir :

- **Des règles de décision métier** (ex. « Un flag non documenté mais activable = MEDIUM »).
- **Des commandes exactes** (`git remote prune origin`, `kiva preflight --no-avx`).
- **Des exemples d’utilisation réalistes** avec des noms de dépôts, des cibles, des workflows.
- **Des formats de sortie attendus** (tableaux, YAML, Markdown).

#### b) Pas de doublons

Plusieurs skills partagent le même contenu, notamment les 6 skills « diagram » (`diagram-vega`, `diagram-uml`, etc.). Chaque skill doit avoir sa **propre syntaxe, ses propres outils, ses propres règles**. Idem pour `lecun-prd` vs `lecun-vision` : l’un devrait générer un PRD, l’autre expliquer la vision. Actuellement ils sont quasi identiques.

#### c) Indentation propre

Dans plusieurs fichiers, des listes sont indentées de 4 espaces, ce qui crée des blocs de code Markdown involontaires. Il faut **uniformiser l’indentation à 2 espaces** (ou pas d’indentation du tout pour les listes simples).

#### d) Format de sortie clair

- Utiliser des code fences avec le bon langage (`yaml`, `bash`, `markdown`) pour les exemples de sortie.
- Structurer le corps avec des sections fixes : `## Domaine et périmètre`, `## Méthodologie`, `## Règles de décision`, `## Format de sortie`, `## Exemples d’utilisation`, `## Intégration avec l’écosystème`.

---

### 4. Retour sur le script PS1 initial

| Aspect | Résultat |
|--------|----------|
| **Génération du ZIP** | Fonctionnelle, 53 fichiers produits |
| **Frontmatter YAML** | Correct, mais sans `\` |
| **Corps détaillés** | 11 skills ont reçu un contenu spécifique (NEXUS, Triade, RepoScope, PLIX, LeCun, Z600…) |
| **Corps génériques** | 32 skills ont reçu le `$body_standard` passe-partout → inutilisables en l’état |
| **Doublons** | Au moins 6 skills diagram et quelques recouvrements (LeCun, RepoScope) |
| **Indentation** | Non maîtrisée, héritée des heredoc PowerShell |

**Le script a été un bon prototype**, mais il aurait dû être suivi d’une relecture manuelle et d’un enrichissement de chaque skill avec les connaissances réelles de l’écosystème.

---

### 5. Enseignements pour la création future de skills Perplexity

1. **Toujours utiliser le `|`** après le frontmatter, sans exception.
2. **Ne jamais utiliser de template générique** – un skill sans contenu spécifique est inutile.
3. **Écrire chaque skill “à la main” ou avec un assistant qui a accès au contexte réel** (dépôts, workflows, commandes). Un LLM sans mémoire produit du remplissage.
4. **Vérifier l’absence de doublons** : deux skills avec le même titre ou le même corps doivent être fusionnés ou différenciés.
5. **Tester l’upload immédiatement** sur un échantillon pour détecter les erreurs de parsing.
6. **Uniformiser la structure** pour que les utilisateurs sachent à quoi s’attendre.
7. **Soigner les déclencheurs** dans la description : lister les mots-clés exacts qui activeront le skill.

---

### 6. Prochaines étapes si on reprenait le projet

- **Passe 1** : Corriger syntaxiquement les 43 fichiers sans `|` (ajouter le `|` + corriger l’indentation).
- **Passe 2** : Remplacer les 32 corps génériques par du contenu spécifique, en s’appuyant sur la documentation existante de l’écosystème (ADR, PRD, README).
- **Passe 3** : Fusionner ou spécialiser les doublons (diagrammes, LeCun, RepoScope Watch/Process).
- **Passe 4** : Générer un nouveau script PS1 *corrigé* qui produit directement les 53 fichiers valides et bien remplis, prêt à être réutilisé.

Si tu le souhaites, je peux attaquer la Passe 1 immédiatement, ou générer un nouveau script complet avec toutes les corrections intégrées.