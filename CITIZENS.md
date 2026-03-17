# CITIZENS — Skills Registry Citizenship

**Version** : 1.0.0 · **Date** : 2026-03-17

## Citoyen: skills-registry

### Identité

| Attribut | Valeur |
|----------|--------|
| **Nom** | skills-registry |
| **Niveau** | L2 |
| **Type** | Registry |
| **Lifecycle** | GENESIS |
| **φ-CPS Weight** | 0.008 |

### Mission

Le citoyen `skills-registry` est responsable de :

1. **Gouvernance** : Maintenir le registre canonique de tous les skills ecosystem-1
2. **Validation** : Vérifier la conformité des skills soumis
3. **Intégration** : Orchestrer l'intégration avec ECOYSTEM
4. **Documentation** : Tenir à jour la taxonomie et la documentation

### Lifecycle

```
GENESIS → ACTIVE → EVOLVING → MATURE → DEPRECATED
```

**Statut actuel** : GENESIS (2026-03-17)

#### Étapes du Lifecycle

| Phase | Description | Critères de Passage |
|-------|-------------|---------------------|
| **GENESIS** | Création initiale | ✅ Dépôt créé, fichiers racine présents |
| **ACTIVE** | Opérationnel | ≥6 skills registered, CI opérationnel |
| **EVOLVING** | En évolution | ≥1 external skill assimilated |
| **MATURE** | Mature | ≥10 skills, ≥3 consumers |
| **DEPRECATED** | Déprécié | Remplacé par un nouveau registre |

### Rights & Responsibilities

#### Rights (Droits)

- ✅ Soumettre des PRs sans approval préalable
- ✅ Valider les skills soumis par d'autres
- ✅ Accéder aux événements WAL
- ✅ Participer aux votes governance

#### Responsibilities (Responsabilités)

- 🔒 Maintenir REGISTRY.yaml à jour
- 🔒 Valider les frontmatter YAML
- 🔒 Vérifier les dépendances entre skills
- 🔒 Signaler les drifts φ-CPS

### φ-CPS Contribution

| Composant | Contribution |
|-----------|--------------|
| Citoyen creation | +0.008 |
| Skill foundational (x2) | +0.010 |
| Skill domain (x4) | +0.020 |
| Documentation | +0.001 |
| **Total** | **+0.039** |

### Relations

#### Providers (Fournisseurs)

| Citoyen | Type | Dépendance |
|---------|------|------------|
| ecoystem-orchestrator | L5 | Gouvernance globale |

#### Consumers (Consommateurs)

| Dépôt | Skill consommé |
|-------|----------------|
| FLUENCE | content, product-context |
| BRAIN | ecosystem-principles, content |
| CANDIDATOR | recruitment, product-context |
| GERIBOOKING | booking |
| BANK-BUSTER | finance |

### Events WAL

Ce citoyen génère les événements suivants :

| Event | Trigger | Données |
|-------|---------|---------|
| `SKILL_CREATED` | Nouveau skill ajouté | skill_name, version, type |
| `SKILL_UPDATED` | Skill mis à jour | skill_name, old_version, new_version |
| `SKILL_DEPRECATED` | Skill déprécié | skill_name, reason |
| `REGISTRY_SYNC` | Synchronisation | skills_count, timestamp |
| `VALIDATION_FAILED` | Échec validation | skill_name, errors |

### Gardes (Guardrails)

| Garde | Seuil | Action |
|-------|-------|--------|
| φ-CPS drift | >5.0% | Alerte + freeze merge |
| Duplicate skills | >0 | Reject PR |
| Broken links | >0 | Reject PR |
| Missing frontmatter | >0 | Reject PR |

### Contact

- **Slack** : #skills-registry
- **GitHub** : @gerivdb/skills-registry
- **WAL Channel** : skills-events

---

*Part of ecosystem-1 governance · Document généré automatiquement*
