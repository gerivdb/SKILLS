---
name: strata-audit-runner
description: "Depuis Perplexity, pilote l'execution de strata_audit.py, lit le rapport de divergences, propose les corrections local_path dans known_repositories.yaml, emet le patch."
version: "1.0.0"
triggers:
  - "strata audit"
  - "audit strate"
  - "verifier local_path"
  - "known_repositories alignment"
  - "strate filesystem"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "STRATA", "AUDIT"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — complement de env-capability-probe (verification specifique strate)"}
slotWeight: 1
trit_primitive: TritCheckConfig
---

# STRATA-AUDIT-RUNNER — Audit strate ↔ filesystem

## Domaine et perimetre

Ce skill pilote l'execution de `strata_audit.py` depuis Perplexity, lit le rapport de divergences, et propose les corrections `local_path` dans `known_repositories.yaml`. Complement de `env-capability-probe` (qui teste ENV2 en general) avec une verification specifique strate ↔ filesystem.

## Methodologie

### Phase 1 — Executer strata_audit.py

```
EXECUTE scripts/strata_audit.py
→ Scan les local_path de known_repositories.yaml
→ Compare avec les dossiers physiques ENV2
→ Produit rapport {present: [...], missing: [...]}
```

### Phase 2 — Lire le rapport

```
[STRATA_AUDIT] Present: N/M
[STRATA_AUDIT] Missing: <liste>
[STRATA_AUDIT] Coverage: X%
```

### Phase 3 — Proposer corrections

Pour chaque repo manquant :
- Verifier si le repo existe sous un autre path
- Proposer la correction `local_path` dans `known_repositories.yaml`
- Si le repo n'existe pas du tout → signaler pour creation ou deprecation

### Phase 4 — Emettre le patch

```
PATCH gerivdb/GOVERNANCE-HUB/known_repositories.yaml
→ Corriger les local_path divergents
→ Mettre a jour metadata.last_updated
```

## Regles de decision

- **Regle 1** : Ne jamais supprimer une entrée sans confirmation
- **Regle 2** : Corriger uniquement les local_path, pas les noms de repos
- **Regle 3** : Si coverage < 80% → alerter (possible deménagement de strate)

## Integration

- **Declencheur** : Apres chaque creation de repo, apres chaque migration de strate
- **Dependances** : Acces ENV2 (execution locale) ou rapport pre-genere
- **Complement de** : env-capability-probe
