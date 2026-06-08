---
name: keel-peg-parser
version: "1.0.0"
description: "Parser PEG pour KEEL v0.5 dans BRAIN. Parse les expressions KEEL (Trit-Nodes, Thought-Commits, TQL, foncteurs, D4 Gate) en AST + IR. Valide les lois R9 (composition/identité) et R10 (D4 gate). Utiliser quand l'utilisateur mentionne 'parser KEEL', 'implémenter foncteur', 'KEEL PEG', 'AST KEEL', 'Thought-Commit', 'TQL live'."
triggers:
  - "parser KEEL"
  - "implémenter foncteur"
  - "KEEL PEG"
  - "AST KEEL"
  - "Thought-Commit"
  - "TQL live"
  - "keel parser"
  - "diamond commit"
layer: "L1_SOT"
nexusTags: ["CONFORME_NEXUS", "KEEL"]
prerequisites:
  - "gerivdb/BRAIN/src/brain/parsers/ (keel_ast.py, keel_lexer.py, keel_parser.py, keel_validator.py)"
  - "gerivdb/BRAIN/src/brain/ir/keel_ir.py"
  - "gerivdb/KEEL/README.md v0.5"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — parser PEG KEEL v0.5"}
trit_primitive: TritIsolate
---

# KEEL-PEG-PARSER — Parser PEG pour KEEL v0.5

## Domaine et périmètre

Ce skill documente et guide l'implémentation du **parser PEG** pour KEEL v0.5 dans BRAIN. Il couvre la grammaire, l'AST, le lexer, le validateur, et le générateur IR.

**Implémentation de référence** : `gerivdb/BRAIN` commit `7725aff`

## Grammaire KEEL v0.5

### Trit-Node
```
[NOM:ETAT:VAGUE@ENV]
Exemple: [ADR:VALIDE:3@ENV2]
```

### Thought-Commit
```
diamond sha7 scope :: "intent description"
Exemple: diamond abc1234 scope :: "audit governance structure"
```

### TQL v0.5
```
FIND .functor:𝔽 WHERE ≋ composition DEPTH T3 AT ENV2
FIND ◈ WHERE ~sim:"description" DEPTH T3
FIND 𝔹ranch WHERE .adjoint:𝔹ranch⊣𝕄erge DEPTH T3
```

### Foncteurs
```
𝔽 [source_verse → target_verse] {
    obj: mapping
    mor: mapping
    ≋ composition
    ≋ identite
}

𝔽ᵒᵖ [source → target] { ... }  # contravariant

η : 𝔽 ⟹ 𝔾 {
    composante_A: mapping
    ≋ carré_commutatif
}

𝔹ranch ⊣ 𝕄erge {
    unité: id ⟹ Merge ∘ Branch
    coünité: Branch ∘ Merge ⟹ id
    ⊷! [FLUX]
}
```

### D4 Gate
```
⊷! [FLUX]
```

## Architecture du parser

```
Source KEEL → Lexer → Tokens → PEG Parser → AST → Validator → IR → BRAIN
```

### Structure des fichiers

```
BRAIN/src/brain/parsers/
├── __init__.py          # API publique (parse, validate, to_ir)
├── keel_ast.py          # Définitions AST
├── keel_lexer.py        # Tokenizer Unicode
├── keel_parser.py       # Parser PEG principal
└── keel_validator.py    # Validation lois R9/R10

BRAIN/src/brain/ir/
└── keel_ir.py           # Générateur IR

BRAIN/tests/
├── test_keel_parser.py  # 20+ tests unitaires
└── test_keel_vdb.py     # 15+ tests VDB
```

## API publique

```python
from parsers import parse, validate, to_ir, parse_and_validate, parse_to_ir

# Parse seulement
ast = parse("[ADR:VALIDE:3@ENV2]")

# Parse + validate
ast, is_valid, errors, warnings = parse_and_validate(source)

# Parse + validate + IR
ir, is_valid, errors = parse_to_ir(source)
```

## Règles de validation

| Règle | Description | Message d'erreur |
|-------|-------------|------------------|
| R9 | Foncteur partiel interdit — doit déclarer ≋ composition ET ≋ identite | "≋ composition manquante" / "≋ identite manquante" |
| R10 | Adjonction Branch⊣Merge doit avoir ⊷! FLUX | "⊷! FLUX manquant" |

## Critères d'acceptation

| Critère | Test |
|---------|------|
| Trit-Node valide | `parse("[ADR:VALIDE:3@ENV2]")` → AST correct |
| Thought-Commit valide | `parse('diamond abc1234 scope :: "test"')` → AST correct |
| TQL valide | `parse("FIND .functor:𝔽 WHERE ≋ composition DEPTH T3")` → AST correct |
| Foncteur valide | Les deux lois ≋ composition + ≋ identite présentes |
| Foncteur invalide | Loi manquante → erreur explicite |
| D4 Gate vérifié | `parse("⊷! [FLUX]")` → AST correct |
| IR produit | `to_ir(ast)` → dict sérialisable |

## Intégration avec l'écosystème

- **Dépôts concernés** : BRAIN (parser), KEEL (spec), NEXUS (IntentHash)
- **Couche EECS** : L1_SOT
- **Skills dépendants** : keel-vdb-tql (utilise l'AST pour l'indexation)
- **Tags NEXUS** : [CONFORME_NEXUS], [KEEL]
