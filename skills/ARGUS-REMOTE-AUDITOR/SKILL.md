# Skill: ARGUS-REMOTE-AUDITOR

## Contexte
Les remotes Git déclarés dans `known_repositories.yaml` peuvent diverger de la réalité GitHub (renommage, fork, suppression). Cette dette silencieuse cause des push rejetés.

## Règle
Pour tout repo avant premier push :
1. Lire `remote` dans `known_repositories.yaml` ou `repos.json`
2. Exécuter `git remote -v` dans `<local_path>`
3. Comparer les deux valeurs
4. Si mismatch ou 404 GitHub : émettre WAL event `REMOTE_MISMATCH`
5. Mettre à jour `repos.json` avec `canonical_remote` validé
6. Ne jamais pousser vers un remote non validé

## Audit périodique
- Cron : vérifier tous les repos avec `git ls-remote --heads <remote> main`
- Si 404 : marquer `REMOTE_BROKEN` dans `repos.json`
- Alerter si un repo a `local_path` valide mais remote cassé

## Anti-pattern interdit
- Pousser vers un remote hypothétique sans validation
- Ignorer un 404 et tenter un rebase/push à l'aveugle
- Créer un nouveau remote sans vérifier l'existence GitHub

## Exemple d'application
```
Repo : diff0-fork
→ known_repositories.yaml : remote: gerivdb/diff0-fork
→ git remote -v : origin https://github.com/gerivdb/diff0.git
→ mismatch détecté → WAL event REMOTE_MISMATCH
→ repos.json mis à jour avec canonical_remote: gerivdb/diff0
→ push vers origin validé
```
