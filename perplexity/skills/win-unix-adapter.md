---
trit_primitive: TritResolvePath
---
# win-unix-adapter

## Objectif
Fournir les équivalents PowerShell des commandes Unix courantes pour ENV2 (Windows).

## Table de mapping

| Unix | PowerShell équivalent |
|---|---|
| `head -n N file` | `Get-Content file \| Select-Object -First N` |
| `tail -n N file` | `Get-Content file \| Select-Object -Last N` |
| `grep pattern file` | `Select-String -Pattern pattern -Path file` |
| `grep -r pattern dir` | `Get-ChildItem -Recurse dir \| Select-String pattern` |
| `wc -l file` | `(Get-Content file).Count` |
| `cat file` | `Get-Content file` |
| `find . -name pattern` | `Get-ChildItem -Recurse -Filter pattern` |
| `rm file` | `Remove-Item file` |
| `rm -rf dir` | `Remove-Item -Recurse -Force dir` |
| `cp src dst` | `Copy-Item src dst` |
| `mv src dst` | `Move-Item src dst` |
| `touch file` | `New-Item file -ItemType File` |
| `which cmd` | `Get-Command cmd` |
| `echo $VAR` | `Write-Output $env:VAR` |
| `export VAR=val` | `$env:VAR = 'val'` |
| `python3` | `python` |

## Règle
Sur ENV2, toujours utiliser la colonne PowerShell. Ne jamais assumer que les outils Unix sont disponibles sans vérification.
