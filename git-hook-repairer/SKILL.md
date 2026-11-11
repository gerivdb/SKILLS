# Skill : git-hook-repairer

## Objectif
Réparer les hooks Git (`.githooks/`) corrompus ou mal formatés sur Windows, en particulier les fichiers de hook sans extension qui sont des scripts batch (`@echo off`) au lieu de scripts shell POSIX avec shebang `#!/bin/sh`. Garantit que `git commit` et `git push` fonctionnent **sans** `--no-verify`.

## Déclencheur
- Hooks Git qui échurent sous Windows car ce sont des fichiers batch au lieu de scripts shell
- Utilisation forcée de `--no-verify` pour contourner des hooks cassés (violation BDCP)
- Erreurs "bad interpreter" ou "syntax error near unexpected token" lors de `git commit`/`git push`

## Protocole de réparation

### Étape 1 — Diagnostiquer les hooks cassés

```powershell
# Vérifier le hooksPath
git -C <repo> config core.hooksPath

# Vérifier le contenu des hooks sans extension
Get-Content <repo>\.githooks\pre-commit
Get-Content <repo>\.githooks\pre-push
Get-Content <repo>\.githooks\commit-msg

# Détecter les fichiers batch (sans shebang #!/bin/sh)
Select-String -Path "<repo>\.githooks\*" -Pattern "^@echo off|^rem |^::"
```

### Étape 2 — Remplacer les hooks batch par des scripts shell

Pour chaque hook sans extension qui est un batch file, le remplacer par :

```sh
#!/bin/sh
pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/<nom>.ps1" "$@"
```

Exemple pour `pre-commit` :
```sh
#!/bin/sh
pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/pre-commit.ps1" "$@"
```

Exemple pour `pre-push` :
```sh
#!/bin/sh
pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/pre-push.ps1" "$@"
```

Exemple pour `commit-msg` :
```sh
#!/bin/sh
pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/commit-msg.ps1" "$1"
```

### Étape 3 — Forcer les fins de ligne LF (Unix)

Sur Windows avec `core.autocrlf = input`, les fichiers de travail peuvent avoir des CRLF. Les hooks Git doivent avoir des LF purs pour être exécutés par le shell Git.

```powershell
# Forcer LF sur tous les hooks sans extension
Get-ChildItem "<repo>\.githooks\*" -File | Where-Object { $_.Extension -eq '' } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace "`r`n", "`n"
    Set-Content -Path $_.FullName -Value $content -NoNewline
}
```

Ou avec `sed` (si disponible) :
```bash
sed -i 's/\r$//' <repo>/.githooks/pre-commit <repo>/.githooks/pre-push <repo>/.githooks/commit-msg
```

### Étape 4 — Rendre les hooks exécutables

```powershell
# Sur Windows avec Git, s'assurer que les hooks ont le bit exécutable
git -C <repo> update-index --chmod=+x .githooks/pre-commit .githooks/pre-push .githooks/commit-msg
```

### Étape 5 — Tester sans --no-verify

```powershell
# Créer un fichier de test, l'ajouter, et committer sans --no-verify
echo "test" > test-hook.txt
git -C <repo> add test-hook.txt
git -C <repo> commit -m "test: valider les hooks réparés"
# Le hook doit s'exécuter sans erreur et sans --no-verify
```

## Invariants de stase

- $\mathcal{F} = 0.0$ : aucune dérive fonctionnelle ; les hooks remplissent le même rôle que les scripts PowerShell sous-jacents
- $\mathcal{H} = 0.0$ : aucune hallucination de spécification ; le remplacement est mécanique (batch → shell wrapper)

## Référence ADR
- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE (règle BDCP)
- **Interdiction** : utilisation de `--no-verify` pour contourner des hooks cassés

## Cas d'usage documenté

| Dépôt | Problème | Correction |
|-------|----------|------------|
| BDCP-CORE | `.githooks/pre-commit` = batch `@echo off` | Remplacer par `#!/bin/sh` + appel `pre-commit.ps1` |
| BDCP-CORE | `.githooks/pre-push` = batch `@echo off` | Remplacer par `#!/bin/sh` + appel `pre-push.ps1` |
| BDCP-CORE | `.githooks/commit-msg` = batch `@echo off` | Remplacer par `#!/bin/sh` + appel `commit-msg.ps1` |
| GOVERNANCE-HUB | Déjà correct (`#!/bin/sh`) | Aucune action requise |
