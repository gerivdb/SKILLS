---
name: branch-audit-cleanup
description: "Audit des branches locales GOVERNANCE-HUB en debut de session. Detecte les orphelines, les doublons de commits, les branches mergeees non supprimees. Utiliser en debut de toute session impliquant GOVERNANCE-HUB."
version: "1.0.0"
triggers:
  - "debut session GOVERNANCE-HUB"
  - "audit branches"
  - "nettoyage branches"
  - "branche orpheline"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "BRANCH_AUDIT", "CLEANUP"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Creation — remede L6/L9 ADR MC-RNN closure"}
slotWeight: 1
---

# BRANCH-AUDIT-CLEANUP — Audit des branches locales

## Domaine et perimetre

Ce skill audite les branches locales de GOVERNANCE-HUB (et autres repos) pour detecter :
- Branches orphelines (sans PR ou merge associe)
- Doublons de commits (meme contenu, SHA different)
- Branches mergeees non supprimees
- Branches avec des commits en avance sur main mais without PR ouverte

Cree comme remede aux lacunes L6 et L9 de la session MC-RNN.

## Methodologie

### Phase 1 — Lister toutes les branches

```bash
git -C "<repo>" branch -a --sort=-committerdate
```

### Phase 2 — Detecter les orphelines

Pour chaque branche locale (hors main/master) :
- Verifier si une PR GitHub ouverte lui est associee
- Verifier si elle a ete mergee (`git branch --merged main`)
- Si mergee et pas encore supprimee → proposer suppression
- Si pas de PR et pas mergee et ancienne (>7j) → signaler orpheline

### Phase 3 — Detecter les doublons de commits

```bash
git -C "<repo>" log --all --oneline | sort | uniq -d
```

Si doublon → identifier les SHAs et proposer suppression du doublon.

### Phase 4 — Rapport

```
[BRANCH_AUDIT] Branches locales : N
[BRANCH_AUDIT] Mergees non supprimees : N
[BRANCH_AUDIT] Orphelines (>7j) : N
[BRANCH_AUDIT] Doublons commits : N
[BRANCH_AUDIT] Actions requises : <liste>
```

## Regles de decision

- **Regle 1** : Branche mergee + pas de PR active → SUPPRIMER
- **Regle 2** : Doublon de commit → SUPPRIMER le plus recent (garder l'original)
- **Regle 3** : Orpheline >30j sans activite → demander confirmation avant suppression
- **Regle 4** : Ne jamais supprimer main/master

## Integration

- **Declencheur** : Debut de session GOVERNANCE-HUB
- **Dependances** : Acces GitHub API pour verifier les PRs
- **Reference ADR** : adr-mc-rnn-closure-20260607.md (lacunes L6, L9)
