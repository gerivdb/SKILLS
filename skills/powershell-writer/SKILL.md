# Skill: powershell-writer

## Contexte
PowerShell exige une syntaxe stricte pour les here-strings. Un header `@'` mal place casse l'ecriture et genere des `ParserError`.

## Regles
1. **Toujours** utiliser la forme : `$content = @'...'@` (variable d'abord, here-string ensuite)
2. **Toujours** finir la ligne du header `@'` par `-Value` ou affectation, pas de caracteres apres
3. Interdire : `Set-Content -Value @'...'` inline
4. Si le fichier cible existe, faire un `Read` prealable pour verifier le contenu avant `Write`
5. Pour les fichiers longs (> 100 lignes), utiliser `write` via outil natif plutot que `bash`

## Formes autorisees
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
'@ 'chemin'  # [KO] ParserError
```

## Anti-pattern interdit
- Header `@'` en debut de ligne de commande
- Melanger here-string et parametres sur la meme ligne
- Utiliser `Out-File` avec here-string sans encodage explicite

## Exemple d'application
```
# AVANT (echec)
Set-Content -Value @'
---
type: PRD
...
'@ 'PRD\file.md'

# APRES (succes)
$content = @'
---
type: PRD
...
'@
Set-Content -LiteralPath 'PRD\file.md' -Value $content
```
