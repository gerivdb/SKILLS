---
name: powershell-json-safe
description: Manipule du JSON complexe en PowerShell en preservant les cles originales via PSObject.Properties. Utilise ce skill quand tu dois lire, ecrire, filtrer ou modifier des JSON PowerShell sans perdre les cles dynamiques.
version: 1.0.0
intent_hash: 0xPOWERSHELL_JSON_SAFE_20260810
---

# PowerShell JSON Safe

## Objectif
Eviter la corruption de JSON PowerShell quand les cles sont dynamiques (IDs, timestamps, noms variables).

## Probleme resolu
`ConvertTo-Json`/`ConvertFrom-Json` sur des `PSCustomObject` perd les cles d'ID quand on filtre avec `Where-Object` car le resultat devient un tableau, pas un objet.

## Regles

### 1. Toujours utiliser PSObject.Properties pour preserver les cles
```powershell
# [KO] DANGEREUX - perd les cles
$filtered = $obj.sessions | Where-Object { $_.worktreeId -ne $null }
$obj.sessions = $filtered  # Devient un tableau, cles perdues

# [OK] SUR - preserve les cles
$newSessions = @{}
foreach ($p in $obj.sessions.PSObject.Properties) {
    if ($p.Value.worktreeId -ne $null) {
        $newSessions[$p.Name] = $p.Value
    }
}
$obj.sessions = [PSCustomObject]$newSessions
```

### 2. Pour les tableaux de hash, utiliser des tables de hachage explicites
```powershell
# [KO] DANGEREUX - tableau de PSCustomObject sans cles
$items = $data | Where-Object { $_.active } | ForEach-Object { $_ }

# [OK] SUR - table de hachage avec cles preservees
$newItems = @{}
foreach ($p in $data.PSObject.Properties) {
    if ($p.Value.active) {
        $newItems[$p.Name] = $p.Value
    }
}
$data.items = [PSCustomObject]$newItems
```

### 3. Pour ConvertTo-Json, toujours preciser Depth
```powershell
# [KO] DANGEREUX - depth par defaut trop faible
$json = $obj | ConvertTo-Json

# [OK] SUR - depth suffisant
$json = $obj | ConvertTo-Json -Depth 10
```

### 4. Verifier la structure apres modification
```powershell
# Apres modification, verifier que les cles sont intactes
$keys = $obj.PSObject.Properties.Name
if ($keys -notcontains 'expectedKey') {
    throw "JSON corruption detected: expectedKey missing"
}
```

## Anti-patterns bloquants
- `$obj.prop = $obj.prop | Where-Object { ... }` sur des objets dynamiques
- `ConvertTo-Json` sans `-Depth` sur des structures profondes
- Acceder a `.Count` directement sur `PSObject.Properties` sans wrapper tableau
- Traiter `PSObject.Properties` comme un tableau sans `@()` ou `foreach`

## Reference ADR
- **ADR** : ADR-2026-08-10-002-POWERSHELL-JSON-SAFE
- **IntentHash** : 0xPOWERSHELL_JSON_SAFE_20260810
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed
