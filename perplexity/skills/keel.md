---
name: keel
description: >-
  KEEL — Knowledge Encoding & Execution Language. Langue de flux ternaire,
  Thought-Commits (◈), TQL (Ternary Query Language), profondeur PLIX ×5 (T1→T5),
  base-243, opérateurs ETE (⊕⊗⊘). Utiliser quand l'utilisateur mentionne
  'KEEL', 'Thought-Commit', 'TQL', 'trit-node', 'flux ternaire', 'PLIX profondeur',
  'base-243 flux', 'DSL ternaire', '◈ commit', 'IntentHash flux'.
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-06-02", notes: "Création initiale — KEEL v0.3 stabilisé, repo créé, GOVERNANCE-HUB enregistré"}
triggers:
  - KEEL
  - Thought-Commit
  - TQL
  - trit-node
  - flux ternaire
  - PLIX profondeur
  - DSL ternaire
layer: "L1b"
nexusTags: ["CONFORME_NEXUS"]
intent_hash: "0xKEEL_NAMING_20260602"
repo: https://github.com/gerivdb/KEEL
---

# KEEL — Knowledge Encoding & Execution Language

## Domaine et périmètre

KEEL est la **langue de représentation de flux** de l'écosystème gerivdb (L1b).
Elle permet d'articuler, historiser et versionner tout flux — raisonnement,
architecture, signal, opération — comme des commits Git, avec :
- Substrat **ternaire base-243** (−/○/+, pentades 5 trits)
- **Thought-Commits** (◈) : unités atomiques de raisonnement versionné
- **TQL** (Ternary Query Language) : requêtes natives sur base-243 + LYCOS + VDB
- **Profondeur PLIX ×5** : T1 surface → T5 temporel
- **Opérateurs ETE** : ⊕ FUSION, ⊗ FISSION, ⊘ CONTINGENCE

KEEL **n'est pas** un exécuteur — c'est un DSL. L'exécution appartient à BRAIN.

---

## Triangle fondateur

```
        KEEL (description + exécution future)
           /              |              \
    base-243          LYCOS             VDB/PLIX
  (valeur ternaire)  (index structurel) (profondeur vectorielle)
           \              |              /
                  TQL (requêtes)
```

---

## Règles critiques (toujours actives)

- **KEEL-R1** — KEEL est un DSL de description. L'exécution = BRAIN. `[CRITICAL]`
- **KEEL-R2** — Tout diagnostic T1-seul est INTERDIT. Minimum T1+T3 croisés. `[CRITICAL]`
- **KEEL-R3** — Tout ◈ doit avoir un IntentHash dans NEXUS. `[HIGH]`
- **KEEL-R4** — TQL ne promeut vers NEXUS que via gate D4 (⊷! FLUX). `[CRITICAL]`
- **KEEL-R5** — Noms dans [NOM] validés par ONTOLOGY avant usage. `[HIGH]`

---

## Primitives KEEL v0.3

### Trit-Node
```
[NOM:ÉTAT:VAGUE@ENV]
[NEXUS:+:V4@ENV2]   [UAE:○:V3@ENV2]   [ATHENA:⊘:V1@ENV0]
```

### Thought-Commit (◈)
```
◈ [sha7] scope :: « intent »
  ← parent: [sha7] | ∅
  ∷ strate: L<N>   @ENV: ENV<N>
  ≡ IntentHash: 0x...
  Δ {
     T1: [surface_observée]
     T2: [structure_déclarée]        # LYCOS.outline
     T3: [intention_git]             # git log
     T4: [couplage_réel]  I_local=N  # LYCOS.deps
     T5: [thermodynamique]  T=N/sem  # LYCOS.hot
  }
  tag: [CONFORME_NEXUS | À_VALIDER | HORS_NEXUS]
```

### Opérateurs principaux
```
# Flux
→  ⇒  ⟲  ∿       # directionnel, conditionnel, rétroaction, signal faible
⊳  ⊲  ⊷!           # émission IRIS, qualification KRONOS, gate D4 FLUX
⊕  ⊗  ⊘  ▲  ▼    # FUSION, FISSION, CONTINGENCE, ESCALADE, DÉGRADATION
◈  ⌥  ⌀  ⊛  ⟳    # commit, branch, revert, cherry-pick, rebase
⌖  ⊞  ⊟            # requête LYCOS, index snapshot, invalidate
?→  ?~             # requête TQL flux, requête TQL similarité
```

---

## TQL — Ternary Query Language

```tql
FIND  <cible>
WHERE <prédicats>
DEPTH <T1..T5>
AT    <@ENV>
SINCE <sha7 | vague | date>

# Prédicats ternaires
:+  :−  :○  :?   (état inconnu → P1 obligatoire)

# Structurels (LYCOS)
.symbol:<nom>   .import:<mod>   .outline:<type>   .trigram:<q>

# Vectoriels (VDB)
~sim:<sha7>     ~cluster:<tag>
```

### Exemples TQL
```tql
# Repos actifs alimentant BRAIN
FIND [*:+:*] WHERE →* [BRAIN:+:*] DEPTH T4 AT @ENV2

# Repos inconnus — P1 requise
FIND [*:?:*] WHERE DEPTH T1 ONLY
EMIT WARNING "passe P1 obligatoire"

# Violation gate D4
FIND [IRIS:+:*] →* [NEXUS:+:*]
WHERE NOT ⊷! [FLUX]
EMIT ERROR "violation D4"
```

---

## Profondeur PLIX ×5

| Trit | Nom | Question | Outil LYCOS |
|------|-----|----------|-------------|
| T1 | SURFACE | Qu'est-ce qui est observable ? | `codedb_tree` |
| T2 | STRUCTURE | Qu'est-ce qui est organisé ? | `codedb_outline` |
| T3 | INTENTION | Qu'est-ce qui est voulu ? | `git log` + IntentHash |
| T4 | COUPLAGE | Qu'est-ce qui est connecté ? | `codedb_deps` |
| T5 | TEMPOREL | Qu'est-ce qui a évolué ? | `codedb_hot` |

---

## Méthodologie d'utilisation

### Exprimer un état de repo
1. Identifier le Trit-Node : `[NOM:état:VAGUE@ENV]`
2. Vérifier le nom dans ONTOLOGY (KEEL-R5)
3. Croiser T1+T3 minimum (KEEL-R2)
4. Ancrer avec IntentHash si action ◈ (KEEL-R3)

### Formuler une requête TQL
1. Choisir la cible (`FIND`)
2. Définir les prédicats ternaires + structurels
3. Fixer la profondeur PLIX (`DEPTH T1..T5`)
4. Vérifier gate D4 si promotion NEXUS (KEEL-R4)

### Décider une opération ETE
1. ⊕ FUSION : deux repos fusionnent en un nouveau
2. ⊗ FISSION : un repo se scinde en deux
3. ⊘ CONTINGENCE : un repo passe en DORMANT/DEPRECATED
4. Toujours exprimer avec `≡ IntentHash` et `⊷! FLUX`

---

## Format de sortie recommandé

```markdown
## Analyse KEEL — [NOM:ÉTAT:VAGUE@ENV]

### Trit-Nodes concernés
- [REPO_A:+:V4@ENV2] → [REPO_B:○:V3@ENV2]

### Thought-Commit proposé
◈ [sha7] scope :: « intent »
  ≡ IntentHash: 0x...
  Δ { T1: ... T3: ... T4: I_local=N }
  tag: [CONFORME_NEXUS]

### TQL si requis
FIND [...] WHERE [...] DEPTH T4

### Verdict
[CONFORME_NEXUS | À_VALIDER_NEXUS | HORS_NEXUS]
```

---

## Intégration écosystème

| Brique | Rôle dans KEEL |
|--------|----------------|
| `gerivdb/BRAIN` | Interpréteur cible — parser PEG (v0.4 planifié) |
| `gerivdb/LYCOS` | Runtime structurel : trigram ×538, deps, outline |
| `gerivdb/VDB` | Stockage vectoriel des ◈ Thought-Commits |
| `gerivdb/PLIX` | Substrat profondeur 5 trits T1→T5 |
| `gerivdb/UAE` | Moteur d'attention sur le DAG de ◈ |
| `gerivdb/ONTOLOGY` | Dictionnaire des noms légitimes dans [NOM] |
| `gerivdb/NEXUS` | Registre des ≡ IntentHash |
| `gerivdb/TOPOS` | Contexte @ENV (souveraineté territoriale) |
| `IRIS·KRONOS·FLUX` | Opérateurs ⊳⊲⊷! — Triade + gate D4 |
| `gerivdb/base-243` | Système de valeur (−/○/+), pentades |

## Exemples d'utilisation
- "Décris l'état de BRAIN" → Exprimer `[BRAIN:+:V4@ENV2]` + Thought-Commit T1→T4
- "KEEL commente cette décision d'architecture" → ETE avec ≡ IntentHash + ⊷! FLUX
- "Requête sur les repos actifs" → TQL `FIND [*:+:*] DEPTH T4`
- "Analyse LYCOS du code BRAIN" → `⌖ .trigram:"ternary" IN [BRAIN:+:V4@ENV2]`
- "Historique de raisonnement" → `?~ [sha7] IN VDB DEPTH T3+T5`
