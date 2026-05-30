# STRATUM RELAY — SKILLS (L6)

**VAGUE**: 4 | **Synchro**: 2026-05-30 | **Hub**: gerivdb/LLM-REPO

- **Strate** : `L6` — Memoire & Documentation
- **Role canonique** : SOT capacites — registre des skills — structure tripartite
- **Parent** : L5 (IA distribuee)

## Regles locales
- R1 — SKILLS est le registre des capacites — tout skill y est enregistre.
- R2 — Structure tripartite : natifs/assimiles/externes.
- Anti-pattern: creer un skill sans l'enregistrer dans SKILLS.

## Karpathy-Recall local (Vague 3 — 10Q)
1. MIMIR est decrire comme 'Wiki Atomique Diamond' — qu'est-ce que cela signifie ?
2. BRAIN-DOCS documente uniquement BRAIN — ou va la doc des autres repos ?
3. SKILLS contient 28 skills actifs — quelle est leur structure tripartite ?
4. DOC-UNIV-DEV est une 'base de connaissances R&D' — en quoi differe-t-il de MIMIR ?
5. Quel repo visualise l'architecture L0->L4.5 sous forme diagrammatique ?
6. Quelles sont les 3 categories de skills enregistre dans SKILLS et qui repond a chaque categorie ?
7. Comment un skill enregistre dans SKILLS doit-il etre reference par un L7 interface lors de son execution ?
8. Quelle est la phrase-cle qui differencie un skill natif d'un skill assimile dans le registre ?
9. Dans quelle situation un skill externe devrait-il etre exclu du registre selon la regle R2 ?
10. Quel L7 interface lit et consomme directement les skills enregistres dans SKILLS ?

## Dependances directes
- **Parents (Amont)** : MIMIR / L5 IA distribuee
- **Enfants (Aval)** : L7 interfaces (lisent SKILLS)

## Agents locaux (Vague 4)

```yaml
# .roomodes — profil agent SKILLS
agent: skills-registrar
strate: L6
role: Skill capacity registry
rules: SKILLS/rules/registry_rules.yaml
hub_ref: MIMIR
```

L'agent `skills-registrar` maintient le registre tripartite des capacites et valide l'enregistrement de chaque nouveau skill.

## Auto-conformite (Vague 4)

- **Guard 1 — Registration mandatory** : Tout skill doit etre enregistre dans SKILLS avant usage par un L7.
- **Guard 2 — Tripartite structure** : Chaque skill doit appartenir a exactement une categorie : natif, assimile, ou externe.
- **Guard 3 — No ghost skills** : Les skills non utilises depuis 90j sont archives automatiquement.

## Vague de mise a jour

| Vague | Date | Contenu |
|-------|------|---------|
| V1 | 2026-05-28 | Initialisation structure Phase 7d — 5Q (P0) |
| V2 | 2026-05-29 | Validation tripartite + dependances L5 (P1) |
| V3 | 2026-05-30 | Extension 10Q + section Dependances directes (P1) |
| **V4** | **2026-05-30** | **Agents locaux (.roomodes) + Auto-conformite (3 guards) deployes** |

---

*Genere par `VERSUS/urban_ontology_verse/TOOLS/relay_propagator.py` v4.0*
*UrbanVerse v4.0.0 — gerivdb/VERSUS (L8)*
*IntentHash: 0xPHASE8_SKILLS_V4_20260530*