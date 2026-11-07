---
type: SPEC
version: 1.0.0
intent_hash: 0xSPEC_COMMIT_ATOMIC_GUARD_20261106
status: proposed
wal_id: 0x243
friction: 0.0
entropy: 0.0
seal: WAL-0x243-SPEC-COMMIT-GUARD-PASS
---

# Spécification — commit-atomic-guard

## 1. Objet

Spécifier la règle de garde atomique sur les commits git : refuser tout commit dépassant 3 fichiers modifiés ou espacé de plus de 30 minutes depuis le dernier commit.

## 2. Contexte

Lors de la Phase 3 du PRD-MOC WiCi, des sessions de travail ont duré sans commit intermédiaire, rendant la récupération difficile en cas d'erreur. La règle d'engagement atomique doit être appliquée strictement.

## 3. Règles obligatoires

### R1 — Maximum 3 fichiers par commit
Tout commit ne doit modifier que 1 à 3 fichiers. Si plus de 3 fichiers sont modifiés, créer un commit intermédiaire.

Exemple de bon découpage :
```
git add scripts/do_core.py scripts/ragx_bridge.py
git commit -m "feat(phase2): implement do-core micro-batch executor"
git add scripts/gerivdb_auditor.py scripts/migrate_network_metrics.py
git commit -m "feat(phase1): implement gerivdb-auditor network metrics"
```

### R2 — Maximum 30 minutes entre deux commits
Si une tâche prend plus de 30 minutes, créer un commit WIP intermédiaire :
```
git add -A
git commit -m "WIP: phase3 vault-sync-daemon (in progress)"
```

### R3 — Vérification avant commit
Avant tout `git commit`, exécuter :
```powershell
git status --short
git diff --stat
git log --oneline -3
```

### R4 — Refus automatique
Tout commit > 3 fichiers ou > 30 minutes depuis le dernier commit doit être refusé par le guard, avec message indiquant la règle violée.

## 4. Message de commit

Convention : `type(scope): description`
- `feat` : nouvelle fonctionnalité
- `fix` : correction de bug
- `docs` : documentation
- `chore` : maintenance

Exemple : `feat(phase3): update default_notebook_id with real target notebook`

## 5. Référence ADR

- **ADR** : ADR-099-git-atomic-commit
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
