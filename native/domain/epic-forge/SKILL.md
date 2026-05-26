# EPIC Forge Skill

> **IntentHash**: `0xEPIC_FORGE_SKILL_20260419`  
> **Version**: 1.0.0  
> **Domain**: governance  
> **Type**: domain  
> **Status**: active

---

## Synopsis

Crée, valide, et gère les EPICs selon la nomenclature NEXUS (CONVENTION.md). Utilise `/epic` pour invoquer.

---

## Triggers

- `/epic create <nom>` — Créer un nouvel EPIC
- `/epic validate <epic-id>` — Valider conformité
- `/epic status <epic-id>` — Voir statut
- `/epic link <parent> <sub>` — Lier sub-issue

---

## Convention Reference

```
EPIC-XXX          → Parent (ex: EPIC-001)
EPIC-XXX.Y        → Sub-phase (ex: EPIC-001.1, EPIC-001.-1)
```

### GitHub Issue Format

| Type | Title | Labels |
|------|-------|--------|
| Parent | `EPIC-XXX: <Title>` | `epic`, `<project>`, `priority/*` |
| Sub | `EPIC-XXX.Y: <Phase>` | `<project>`, `phase/*` |

---

## Commands

### Create Parent EPIC

```bash
/epic create PLIX
```

**Generated:**
- File: `EPIC_PLIX_GENESIS.md`
- Issue: `NEXUS#70` (EPIC-001: PLIX GENESIS)

### Create Sub-Phase

```bash
/epic create PLIX -phase -1
```

**Generated:**
- File: `EPIC_PLIX_PHASE_NEGATIVE_1.md`
- Issue: `NEXUS#71` (EPIC-001.1: PLIX Phase -1)

### Validate EPIC

```bash
/epic validate EPIC-001
```

**Checks:**
- [ ] Parent EPIC a un `IntentHash` valide
- [ ] Parent EPIC a une issue GitHub associée
- [ ] Chaque phase a une sub-issue GitHub liée
- [ ] Toutes les sub-issues ont un deadline
- [ ] Les dépendances sont listées
- [ ] IntentHash unique par EPIC/phase

---

## IntentHash Convention

```
0x<PROJECT>_<PHASE>_<DATE>[_<VERSION>]
```

| Component | Description |
|-----------|-------------|
| `PROJECT` | Nom du projet (ex: PLIX) |
| `PHASE` | Phase (ex: PHASE_NEG1, GENESIS) |
| `DATE` | Date YYYYMMDD |

---

## Files Location (NEXUS)

```
NEXUS/epics/
├── INDEX.md           # Central index
├── CONVENTION.md      # Nomenclature
├── SKILL.md           # This skill (reference)
├── EPIC_XXX.md       # Parent EPIC
├── EPIC_XXX_Y.md     # Phases
└── ...
```

---

## Examples

| Command | Result |
|---------|--------|
| `/epic create PLIX` | EPIC-001 + NEXUS issue |
| `/epic create PLIX -phase 0` | EPIC-001.2 + sub-issue |
| `/epic validate EPIC-001` | Validation report |
| `/epic status EPIC-001` | Current phases status |

---

## Dependencies

- SKILLS (skill registry)
- NEXUS (EPIC storage)
- GitHub API (issue management)

---

*IntentHash: 0xEPIC_FORGE_SKILL_20260419 | Version: 1.0.0*