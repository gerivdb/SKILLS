---
type: GUI
version: "2.0.0"
date: "2026-06-08"
intent_hash: 0xREPO_PATH_RESOLVER_V2_20260608
status: active
---

# Skill: repo-path-resolver

## Purpose
Resolve canonical local paths for any repository in the gerivdb ecosystem. ALWAYS use this skill before any cross-repo operation. NEVER guess paths.

## Context
All repos are organized in strata directories (L0-L5) under `D:\DO\WEB\TOOLS\`. The authoritative source for paths is `known_repositories.yaml`. Use the 3-Level Lazy Search: INDEX -> STRATA -> RECURSIVE.

## Regle - 3-Level Lazy Search

### Level 1 - INDEX (toujours en premier)

```powershell
$yaml  = "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\known_repositories.yaml"
$data  = yaml.safe_load(open($yaml, encoding='utf-8'))
foreach ($section in @("P0_CONSTITUTIONAL","P1_STRATEGIC","P2_SUPPORT","P3_DORMANT")) {
    $match = $data[$section] | Where-Object { $_.name -eq $repoName }
    if ($match) { return $match.local_path }
}
```

### Level 2 - STRATA (si Level 1 echoue)

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

### Level 3 - RECURSIO (dernier recours, lent)

```powershell
Get-ChildItem "D:\DO\WEB\TOOLS" -Recurse -Directory -Depth 2 |
    Where-Object { $_.Name -like "*$repoName*" } |
    Select-Object -First 1 -ExpandProperty FullName
```

## Anti-patterns interdits

- **Deduire le chemin depuis le nom du repo** - toujours chercher
- **Chercher uniquement a la racine** `D:\DO\WEB\TOOLS\$repo` - les repos sont dans L0-L5
- **Utiliser `C:\DevTools\<repo>` sans verification**
- **Creer un repertoire si le chemin n'existe pas** sans ordre explicite
- **Recherche recursive en premier** - gaspille des ressources sur 177+ repos

## Checklist pre-operation

- [ ] Level 1 : `known_repositories.yaml` lu -> `local_path` extrait
- [ ] Level 2 : Strata L0-L5 iteres si Level 1 echoue
- [ ] Level 3 : Recherche recursive Depth 2 si Level 2 echoue
- [ ] `Test-Path` confirme avant toute operation
- [ ] Si introuvable apres 3 niveaux -> `REPO_PATH_NOT_FOUND`, ne pas deviner

## Exemple

```
Repo demande : KIVA-CLI
-> Level 1: known_repositories.yaml -> P1_STRATEGIC -> local_path: D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
-> Test-Path : OK
-> Operations sur D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
```

```
Repo demande : FLUENCE
-> Level 1: known_repositories.yaml -> P1_STRATEGIC -> local_path: D:\DO\WEB\TOOLS\L1-INFRA\FLUENCE
-> Test-Path : OK
```
