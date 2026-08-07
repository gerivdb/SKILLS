# Skill: ARGUS-REMOTE-AUDITOR

## Contexte
Les remotes Git declares dans `known_repositories.yaml` peuvent diverger de la realite GitHub (renommage, fork, suppression). Cette dette silencieuse cause des push rejetes.

## Regle
Pour tout repo avant premier push :
1. Lire `remote` dans `known_repositories.yaml` ou `repos.json`
2. Executer `git remote -v` dans `<local_path>`
3. Comparer les deux valeurs
4. Si mismatch ou 404 GitHub : emettre WAL event `REMOTE_MISMATCH`
5. Mettre a jour `repos.json` avec `canonical_remote` valide
6. Ne jamais pousser vers un remote non valide

## Audit periodique
- Cron : verifier tous les repos avec `git ls-remote --heads <remote> main`
- Si 404 : marquer `REMOTE_BROKEN` dans `repos.json`
- Alerter si un repo a `local_path` valide mais remote casse

## Anti-pattern interdit
- Pousser vers un remote hypothetique sans validation
- Ignorer un 404 et tenter un rebase/push a l'aveugle
- Creer un nouveau remote sans verifier l'existence GitHub

## Exemple d'application
```
Repo : diff0-fork
-> known_repositories.yaml : remote: gerivdb/diff0-fork
-> git remote -v : origin https://github.com/gerivdb/diff0.git
-> mismatch detecte -> WAL event REMOTE_MISMATCH
-> repos.json mis a jour avec canonical_remote: gerivdb/diff0
-> push vers origin valide
```
