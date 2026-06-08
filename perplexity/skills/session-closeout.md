---
name: session-closeout
description: "Checklist de cloture de session operationnelle multi-repo (Gate D5). Verifie : PRs merged, branches supprimes, clones orphelins, ECOS_ROOT coherent, ADR de cloture, hooks testes. Utiliser en fin de session."
version: "1.0.0"
triggers:
  - "cloturer session"
  - "fin de session"
  - "gate D5"
  - "session closeout"
  - "checklist cloture"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SESSION_MANAGEMENT", "GATE"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Creation — remede L4 ADR MC-RNN closure"}
slotWeight: 1
trit_primitive: TritDocumentRegister
---

# SESSION-CLOSET — Checklist de cloture multi-repo (Gate D5)

## Domaine et perimetre

Ce skill produit une **checklist de cloture** pour les sessions operationnelles multi-repo. Il verifie que tous les artefacts de la session sont propres avant de declarer la session terminee.

Cree comme remede a la lacune L4 de la session MC-RNN (pas de gate D5 defini).

## Checklist D5 (Gate de cloture)

### Items obligatoires (tous doivent etre coches)

```
□ 1. Toutes les PRs de la session sont merged ou closed
□ 2. Toutes les branches feature/* de la session sont supprimees (local + remote)
□ 3. Aucun clone orphelin dans les paths L4-TOOLS/, L0-CANON/, etc.
□ 4. ECOS_ROOT.json coherent (paths reels verifies, get_file_contents reussi)
□ 5. ADR de cloture cree et push (status: accepted)
□ 6. known_repositories.yaml synchronise avec la realite GitHub
□ 7. Hook pre-commit teste (git commit --allow-empty dans chaque repo modifie)
□ 8. Working trees propres (git status == clean sur chaque repo)
```

### Verification par item

**Item 1 — PRs merged** :
```bash
gh list-pulls --state all --repo gerivdb/<repo>
# Verifier que toutes les PRs de la session sont closed/merged
```

**Item 2 — Branches supprimees** :
```bash
git -C "<repo>" branch -a | grep "feature/"
# Ne doit plus y avoir de branche de session
```

**Item 3 — Clones orphelins** :
```powershell
Get-ChildItem -Path "D:\DO\WEB\TOOLS\L4-TOOLS" -Directory | Where-Object { $_.Name -match "real|old|bak|temp" }
# Aucun clone orphelin
```

**Item 4 — ECOS_ROOT.json** :
- Lire le fichier avec get_file_contents
- Verifier que chaque physical_path existe sur disque
- Verifier qu'aucune entree n'a ete perdue

**Item 5 — ADR cloture** :
- Verifier l'existence de l'ADR de cloture
- Verifier status: accepted

**Item 6 — known_repositories.yaml** :
- Comparer avec les repos GitHub reels
- Supprimer les entrees fantomes

**Item 7 — Hook teste** :
```bash
git commit --allow-empty -m "test: hook verification" --no-verify
# Puis verifier que le hook s'execute sur le prochain commit
```

**Item 8 — Working trees** :
```bash
git -C "<repo>" status --short
# Doit etre vide
```

## Format de sortie

```
=== GATE D5 — Session Closeout ===

[OK]   PRs merged/closed
[OK]   Branches supprimees
[OK]   Pas de clones orphelins
[OK]   ECOS_ROOT.json coherent
[OK]   ADR cloture existe
[OK]   known_repositories.yaml sync
[OK]   Hook teste
[OK]   Working trees propres

Resultat: D5 GATE PASSED
```

Si un item echoue :
```
[BLOCKED] <item> — <raison>
Resultat: D5 GATE BLOCKED
```

## Integration

- **Declencheur** : Fin de session operationnelle multi-repo
- **Dependances** : session-snapshot, branch-audit-cleanup, pre-push-path-audit
- **Reference ADR** : adr-mc-rnn-closure-20260607.md (lacune L4)
