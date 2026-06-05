# Skill: powershell-writer

## Contexte
PowerShell exige une syntaxe stricte pour les here-strings. Un header `@'` mal placé casse l'écriture et génère des `ParserError`.

## Règles
1. **Toujours** utiliser la forme : `$content = @'...'@` (variable d'abord, here-string ensuite)
2. **Toujours** finir la ligne du header `@'` par `-Value` ou affectation, pas de caractères après
3. Interdire : `Set-Content -Value @'...'` inline
4. Si le fichier cible existe, faire un `Read` préalable pour vérifier le contenu avant `Write`
5. Pour les fichiers longs (> 100 lignes), utiliser `write` via outil natif plutôt que `bash`

## Formes autorisées
```powershell
# Forme 1 : variable + Set-Content
$content = @'
ligne 1
ligne 2
'@
Set-Content -LiteralPath 'chemin' -Value $content

# Forme 2 : Write-Output + redirection
@'
ligne 1
ligne 2
'@ | Set-Content -LiteralPath 'chemin'

# Forme interdite
Set-Content -Value @'
...
'@ 'chemin'  # ❌ ParserError
```

## Anti-pattern interdit
- Header `@'` en début de ligne de commande
- Mélanger here-string et paramètres sur la même ligne
- Utiliser `Out-File` avec here-string sans encodage explicite

## Exemple d'application
```
# AVANT (échec)
Set-Content -Value @'
---
type: PRD
...
'@ 'PRD\file.md'

# APRÈS (succès)
$content = @'
---
type: PRD
...
'@
Set-Content -LiteralPath 'PRD\file.md' -Value $content
```
