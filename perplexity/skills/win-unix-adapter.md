---
skill_id: win-unix-adapter
trit_primitive: TritResolvePath
version: 1.1.0
updated: 2026-06-09
status: active
tags: [windows, powershell, unix, env2, z600]
---

# win-unix-adapter

## Purpose
Fournir les équivalents PowerShell des commandes Unix courantes pour ENV2 (Windows Z600).

## Trigger
Use when: user mentions "unix command", "head", "tail", "grep", "wc", "find", "rm", "cp", "mv", "touch", "which", "echo", "export", "python3" on Windows.

## Steps

1. Identify the Unix command from user request
2. Map to the PowerShell equivalent using the table below
3. Execute the PowerShell command on ENV2

## Mapping table

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

## Rules
- On ENV2, always use the PowerShell column — never assume Unix tools are available
- Always verify with `Get-Command` before using any tool
- For `grep -r`, always pipe through `Select-String` — never use `grep` alias

## Output
PowerShell command string ready to execute on ENV2.

## Example

```
User: "Show me the first 10 lines of config.yaml"
→ Get-Content config.yaml | Select-Object -First 10

User: "Find all .md files containing 'intent_hash'"
→ Get-ChildItem -Recurse -Filter *.md | Select-String "intent_hash"

User: "Count lines in known_repositories.yaml"
→ (Get-Content known_repositories.yaml).Count
```
