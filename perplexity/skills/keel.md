---
name: keel
description: >-
  KEEL — Knowledge Encoding & Execution Language. Langue de la complexité
  historique, métacognitive et métamorphique du métacluster gerivdb.
  Thought-Commits (◈), TQL, PLIX×5, base-243, ETE (⊕⊗⊘),
  ◈-DAG (histoire vivante), META-LOOP (réflexivité BRAIN↔KEEL),
  VERSE-MORPH (transformation Verses VERSUS), HARNESS (plasticité BRAIN + BLO).
  Utiliser quand l'utilisateur mentionne 'KEEL', 'Thought-Commit', 'TQL',
  'trit-node', 'flux ternaire', 'PLIX profondeur', 'DSL ternaire',
  '◈-DAG', 'META-LOOP', 'VERSE-MORPH', 'HARNESS', 'plasticité BRAIN',
  'registre BLO', 'Verse émergence', 'dérive φ-CPS', 'boucle réflexive'.
version: "1.1.0"
changelog:
  - {v: "1.0.0", date: "2026-06-02", notes: "Création initiale — KEEL v0.3"}
  - {v: "1.1.0", date: "2026-06-02", notes: "KEEL v0.4 : ◈-DAG + META-LOOP + VERSE-MORPH + HARNESS — 8 règles, 15Q Karpathy"}
triggers:
  - KEEL
  - Thought-Commit
  - TQL
  - trit-node
  - flux ternaire
  - PLIX profondeur
  - DSL ternaire
  - ◈-DAG
  - META-LOOP
  - VERSE-MORPH
  - HARNESS
  - plasticité BRAIN
  - registre BLO
  - Verse émergence
  - dérive phi-CPS
layer: "L1b"
nexusTags: ["CONFORME_NEXUS"]
intent_hash: "0xKEEL_V04_20260602"
repo: https://github.com/gerivdb/KEEL
---

# KEEL — Knowledge Encoding & Execution Language (v0.4)

## Domaine et périmètre

KEEL est la **langue de la complexité vivante** de l'écosystème gerivdb (L1b).
Elle articule, historise et versionne tout flux — raisonnement, architecture,
métamorphose — en 4 couches :

| Couche | Bloc | Adresse |
|--------|------|---------|
| Fondation v0.3 | Trit-Node · ◈ · TQL · PLIX×5 | base-243 + LYCOS + VDB |
| Histoire | **◈-DAG** | dérive φ-CPS, replay, fantômes |
| Métacognition | **META-LOOP** | BRAIN s'observe via KEEL |
| Métamorphose | **VERSE-MORPH** | composition/émergence Verses VERSUS |
| Plasticité | **HARNESS** | plug/unplug BRAIN + registres BLO |

KEEL **n'est pas** un exécuteur — DSL pur. L'exécution appartient à BRAIN.

---

## Règles critiques (8 actives — toujours appliquer)

- **R1** — KEEL = DSL. Exécution = BRAIN. `[CRITICAL]`
- **R2** — T1-seul INTERDIT. Minimum T1+T3 croisés. `[CRITICAL]`
- **R3** — Tout ◈ → IntentHash dans NEXUS. `[HIGH]`
- **R4** — TQL + META-LOOP + HARNESS → gate D4 (⊷! FLUX) pour promotion NEXUS. `[CRITICAL]`
- **R5** — Noms dans [NOM] validés par ONTOLOGY. `[HIGH]`
- **R6** — META-LOOP ⟳ : agent ne peut pas auto-valider sa propre réflexion. `[CRITICAL]`
- **R7** — VERSE-MORPH ◈↗ (nouveau Verse) → ⊷! FLUX + IntentHash. `[HIGH]`
- **R8** — HARNESS ⊲ (BLO) → ⊷! FLUX. Zéro auto-modification BRAIN. `[CRITICAL]`

---

## Primitives v0.3 (fondation)

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
     T1: [surface]       # LYCOS.tree
     T2: [structure]     # LYCOS.outline
     T3: [intention]     # git log
     T4: I_local=N       # LYCOS.deps
     T5: T=N/sem         # LYCOS.hot
  }
  tag: [CONFORME_NEXUS | À_VALIDER | HORS_NEXUS]
```

### TQL
```tql
FIND <cible> WHERE <prédicats> DEPTH <T1..T5> AT <@ENV> SINCE <ref>
# :+  :−  :○  :?  | .trigram: .symbol: .import: | ~sim: ~cluster:
# Nouveau v0.4 : .drift:∿>  .verse:<nom>  .harness:<module>  .blo:<path>
```

### PLIX ×5
| T1 SURFACE | T2 STRUCTURE | T3 INTENTION | T4 COUPLAGE | T5 TEMPOREL |
|------------|--------------|--------------|-------------|-------------|
| `codedb_tree` | `codedb_outline` | `git log` | `codedb_deps` | `codedb_hot` |

---

## Bloc I — ◈-DAG (Histoire vivante)

```keel
◈-DAG [NEXUS] {
  ⟲ vague V1→V4                # rejouer l'histoire
  ∿> drift [BRAIN:φ3.2→φ4.65]  # dérive positive mesurée
  ◈↺ [7b5c100] @ENV2            # replay d'un ◈ dans nouveau contexte
  ◈⊗ [ATHENA←BRAIN]            # conflit fantôme non résolu
}
```

Opérateurs : `∿< ∿> ∿= ◈↺ ◈⊗ ◈∅ ⟲`

---

## Bloc II — META-LOOP (Métacognition)

```keel
META-LOOP [BRAIN:+:V4@ENV2] {
  ⟳ self-observe :: « BRAIN analyse son propre φ-CPS »
    ≡ IntentHash: 0xBRAIN_SELFWATCH_V4
    Δ { T1: [WAL actif] T3: [φ4.650] T4: I_local=KIVA+ECOS-CLI T5: ∿> }

  ⟳ reflect-on :: [KEEL:design:V1@ENV2]
    « BRAIN doit implémenter ce qui le décrit »
    ⊷! [FLUX]   # gate D4 : humain valide le paradoxe
}
```

Opérateurs : `⟳ ⟳² ↯ ⟳→`

> Règle R6 : toute boucle `⟳` → `⊷! FLUX` obligatoire.

---

## Bloc III — VERSE-MORPH (Métamorphose Verses)

```keel
VERSE-MORPH [political_compass_verse → urban_ontology_verse] {
  ⊞ [VERSUS/socioverse]    # composition
  ◉ [BATVERSE]             # projection narrative
  ≋ topology               # invariant conservé
  Δ-verse { T1: [(S,M,E,I)=(2,0,2,1)] T4: I_cross=VERSUS+BRAIN }
}

# Émergence d'un nouveau Verse
VERSE-MORPH {
  ◈↗ [poincare_topology_verse] @L5
    ≋ topology: manifold_ternaire
    ⊞ [BRAIN:attention:UAE]
    ≡ IntentHash: 0xPOINCARE_VERSE_EMERGENCE
    ⊷! [FLUX]   # R7 : obligatoire
}
```

Opérateurs : `⊞ ◉ ≋ ◈↗ ◈↘ ⊷~ ⊛`

---

## Bloc IV — HARNESS (Plasticité BRAIN + BLO)

```keel
HARNESS [BRAIN:+:V4@ENV2] {
  ⌥ plug   [UAE:attention:1/√d]     # brancher module
  ⌥ unplug [cache_manager:LRU]      # débrancher
  ⌥ rewire [KIVA → ECOS-CLI]        # recâbler
  ⌾ φ-CPS: 4.650                    # ancre plasticité

  BLO-sync {
    ⊳ read  [ECOYSTEM/BLO/current]
    ⊲ write [ECOYSTEM/BLO/KEEL-patch-001]   # R8 : ⊷! FLUX obligatoire
    ≡ IntentHash: 0xBRAIN_HARNESS_V4
    ⊷! [FLUX]
  }
}
```

Opérateurs : `⌥ plug/unplug/rewire ⌾ ⊳ ⊲ ⌥↯ ⌾↑ ⌾↓`

---

## Format de sortie recommandé

```markdown
## Analyse KEEL v0.4 — [NOM:ÉTAT:VAGUE@ENV]

### ◈-DAG (histoire)
- dérive : ∿> φX→φY sur N vagues
- fantômes : ◈⊗ [...]

### Thought-Commit proposé
◈ [sha7] scope :: « intent »
  ≡ IntentHash: 0x...
  Δ { T1: ... T3: ... T4: I_local=N }
  tag: [CONFORME_NEXUS]

### META-LOOP (si réflexion requise)
⟳ self-observe :: « ... »  ⊷! [FLUX]

### VERSE-MORPH (si Verse concerné)
VERSE-MORPH { ... ≋ topology }

### HARNESS (si plasticité requise)
HARNESS { ⌥ plug/unplug/rewire ... ⊷! [FLUX] }

### Verdict
[CONFORME_NEXUS | À_VALIDER_NEXUS | HORS_NEXUS]
```

---

## Intégration écosystème v0.4

| Brique | Rôle |
|--------|------|
| `gerivdb/BRAIN` | Interpréteur + plasticité HARNESS + META-LOOP ⟳ |
| `gerivdb/LYCOS` | Runtime structurel (trigram×538, deps, outline) |
| `gerivdb/VDB` | Stockage vectoriel ◈ |
| `gerivdb/PLIX` | Substrat T1→T5 |
| `gerivdb/UAE` | Attention DAG ◈ + plug HARNESS |
| `gerivdb/ONTOLOGY` | Dictionnaire [NOM] |
| `gerivdb/NEXUS` | Registre IntentHash |
| `gerivdb/TOPOS` | Contexte @ENV |
| `gerivdb/VERSUS` | Source Verses pour VERSE-MORPH |
| `gerivdb/ECOYSTEM` | Registres BLO pour HARNESS ⊳⊲ |
| `IRIS·KRONOS·FLUX` | Triade + gate D4 ⊷! |
| `gerivdb/base-243` | Système de valeur −/○/+ |

## Exemples d'utilisation v0.4
- "Quelle est l'histoire de BRAIN ?" → `◈-DAG [BRAIN] { ∿> drift φ3.2→φ4.65 }`
- "BRAIN s'observe" → `META-LOOP ⟳ self-observe :: « ... » ⊷! [FLUX]`
- "Nouveau Verse émerge" → `VERSE-MORPH { ◈↗ [...] ≋ topology ⊷! [FLUX] }`
- "Brancher le parser KEEL dans BRAIN" → `HARNESS { ⌥ plug [KEEL:parser:v0.5] ⊷! [FLUX] }`
- "Lire BLO courant" → `HARNESS { ⊳ read [ECOYSTEM/BLO/current] }`
