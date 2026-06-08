# Skill: repo-path-resolver

## Contexte
Tout agent Kilo opérant cross-repo doit résoudre le chemin canonique d'un repo avant toute opération. La knowledge base des chemins est `known_repositories.yaml`.

## Règle — 3-Level Lazy Search

### Level 1 — INDEX (toujours en premier)

```powershell
$yaml  = "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\known_repositories.yaml"
$data  = yaml.safe_load(open($yaml, encoding='utf-8'))
foreach ($section in @("P0_CONSTITUTIONAL","P1_STRATEGIC","P2_SUPPORT","P3_DORMANT")) {
    $match = $data[$section] | Where-Object { $_.name -eq $repoName }
    if ($match) { return $match.local_path }
}
```

### Level 2 — STRATA (si Level 1 échoue)

```powershell
$strata = @(
    "D:\DO\WEB\TOOLS\L0-CANON",
    "D:\DO\WEB\TOOLS\L1-INFRA",
    "D:\DO\WEB\TOOLS\L2-PLATFORM",
    "D:\DO\WEB\TOOLS\L3-CITIZENS",
    "D:\DO\WEB\TOOLS\L4-TOOLS",
    "D:\DO\WEB\TOOLS\L5-ARCHIVE"
)
foreach ($s in $strata) {
    $candidate = Join-Path $s $repoName
    if (Test-Path $candidate) { return $candidate }
}
```

### Level 3 — RECURSIO (dernier recours, lent)

```powershell
Get-ChildItem "D:\DO\WEB\TOOLS" -Recurse -Directory -Depth 2 |
    Where-Object { $_.Name -like "*$repoName*" } |
    Select-Object -First 1 -ExpandProperty FullName
```

## Anti-patterns interdits

- **Déduire le chemin depuis le nom du repo** — toujours chercher
- **Chercher uniquement à la racine** `D:\DO\WEB\TOOLS\$repo` — les repos sont dans L0-L5
- **Utiliser `C:\DevTools\<repo>` sans vérification**
- **Créer un répertoire si le chemin n'existe pas** sans ordre explicite
- **Recherche récursive en premier** — gaspille des ressources sur 177+ repos

## Checklist pré-opération

- [ ] Level 1 : `known_repositories.yaml` lu → `local_path` extrait
- [ ] Level 2 : Strata L0-L5 itérés si Level 1 échoue
- [ ] Level 3 : Recherche récursive Depth 2 si Level 2 échoue
- [ ] `Test-Path` confirmé avant toute opération
- [ ] Si introuvable après 3 niveaux → `REPO_PATH_NOT_FOUND`, ne pas deviner

## Exemple

```
Repo demandé : KIVA-CLI
→ Level 1: known_repositories.yaml → P1_STRATEGIC → local_path: D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
→ Test-Path : OK
→ Opérations sur D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
```

```
Repo demandé : FLUENCE
→ Level 1: known_repositories.yaml → P1_STRATEGIC → local_path: D:\DO\WEB\TOOLS\L1-INFRA\FLUENCE
→ Test-Path : OK
```
