import sys

path = r'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills\ext-code-reviewer.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'PRE-MERGE GATE' in content:
    print('Pre-merge gate already present')
    sys.exit(0)

addition = """
## PRE-MERGE GATE (obligatoire, cree 2026-06-07)

**Ce gate est OBLIGATOIRE avant tout merge_pull_request(). Aucun merge sans l'avoir execute.**

### Checklist pre-merge

1. **Review diff** : git diff main...<branch> | head -200
2. **Detection doublons** : git log --oneline <branch> | sort | uniq -d
3. **Verification typos fonctions** : grep pour les appels critiques (ex: vector_to_base23 sans le 4)
4. **Verification tests** : les tests de la branche passent-ils ?
5. **Verification frontmatter** : si PRD/ADR modifie, frontmatter valide ?
6. **Verification remote** : push API atterri sur le bon repo ?

### Regles

- Doublon -> REJETER, supprimer le commit doublon
- Typo critique -> REJETER, corriger avant merge
- Tests non executes -> REJETER
- Frontmatter invalide -> REJETER

### Reference

Remede aux lacunes L2 et L9 (ADR adr-mc-rnn-closure-20260607.md).
"""

content = content.rstrip() + '\n' + addition
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pre-merge gate appended to ext-code-reviewer.md')
