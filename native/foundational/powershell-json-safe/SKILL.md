---
name: powershell-json-safe
description: Manipule du JSON complexe en PowerShell en préservant les clés originales via PSObject.Properties. Utilise ce skill quand tu dois lire, écrire, filtrer ou modifier des JSON PowerShell sans perdre les clés dynamiques.
version: 1.0.0
intent_hash: 0xPOWERSHELL_JSON_SAFE_20260810
---

# PowerShell JSON Safe

## Objectif
Éviter la corruption de JSON PowerShell quand les clés sont dynamiques (IDs, timestamps, noms variables).

## Problème résolu
`ConvertTo-Json`/`ConvertFrom-Json` sur des `PSCustomObject` perd les clés d'ID quand on filtre avec `Where-Object` car le résultat devient un tableau, pas un objet.

## Règles

### 1. Toujours utiliser PSObject.Properties pour préserver les clés
```powershell
# ❌ DANGEREUX — perd les clés
$filtered = $obj.sessions | Where-Object { $_.worktreeId -ne $null }
$obj.sessions = $filtered  # Devient un tableau, clés perdues

# ✅ SÛR — préserve les clés
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
# ❌ DANGEREUX — tableau de PSCustomObject sans clés
$items = $data | Where-Object { $_.active } | ForEach-Object { $_ }

# ✅ SÛR — table de hachage avec clés préservées
$newItems = @{}
foreach ($p in $data.PSObject.Properties) {
    if ($p.Value.active) {
        $newItems[$p.Name] = $p.Value
    }
}
$data.items = [PSCustomObject]$newItems
```

### 3. Pour ConvertTo-Json, toujours préciser Depth
```powershell
# ❌ DANGEREUX — depth par défaut trop faible
$json = $obj | ConvertTo-Json

# ✅ SÛR — depth suffisant
$json = $obj | ConvertTo-Json -Depth 10
```

### 4. Vérifier la structure après modification
```powershell
# Après modification, vérifier que les clés sont intactes
$keys = $obj.PSObject.Properties.Name
if ($keys -notcontains 'expectedKey') {
    throw "JSON corruption detected: expectedKey missing"
}
```

## Anti-patterns bloquants
- `$obj.prop = $obj.prop | Where-Object { ... }` sur des objets dynamiques
- `ConvertTo-Json` sans `-Depth` sur des structures profondes
- Accéder à `.Count` directement sur `PSObject.Properties` sans wrapper tableau
- Traiter `PSObject.Properties` comme un tableau sans `@()` ou `foreach`

## Référence ADR
- **ADR** : ADR-2026-08-10-002-POWERSHELL-JSON-SAFE
- **IntentHash** : 0xPOWERSHELL_JSON_SAFE_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
