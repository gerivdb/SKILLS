# M3 Skill — Evidence Auto-Enroller (Auto EVIDENCE.md)
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xM3_SKILL_EVIDENCE_AUTO_ENROLLER_20261123

## Définition
Enregistre automatiquement la preuve d'exécution (EVIDENCE.md) après chaque utilisation d'un skill.
Génère l'entrée EVIDENCE.md avec : date UTC, shard, résultat, code de sortie, hash SHA-256 du résultat, fichiers modifiés.

## Prérequis
- Python 3.10+
- Accès écriture au répertoire du skill et au EVIDENCE.md global

## Déclencheur
- Après exécution réussie d'un skill (code de sortie 0)
- Après commit d'un fichier modifié par un skill
- Après push réussi d'un skill

## GESTES (séquence atomique)

### GESTE-1 — Collecter métadonnées d'exécution
```
- skill_name: nom du skill exécuté
- shard_id: identifiant du shard (ex: ENV2, G)
- command: commande exécutée
- exit_code: code de sortie
- stdout: sortie standard (tronquée à 10KB)
- stderr: erreur standard (tronquée à 10KB)
- duration_ms: durée d'exécution
- files_modified: liste des fichiers modifiés/créés/supprimés
```

### GESTE-2 — Calculer hash SHA-256
```
hash = SHA256(stdout + stderr + json.dumps(files_modified))
```

### GESTE-3 — Générer entrée EVIDENCE.md
Format Markdown :
```markdown
## [TIMESTAMP_UTC] Skill: <skill_name> | Shard: <shard_id> | Exit: <code>
- **Command**: `<command>`
- **Duration**: <duration_ms>ms
- **Hash**: <sha256>
- **Files**: <files_modified>
- **Stdout**: `<stdout_truncated>`
- **Stderr**: `<stderr_truncated>`
```

### GESTE-4 — Écrire dans EVIDENCE.md
- Local: `<skill_dir>/EVIDENCE.md`
- Global: `L4-TOOLS/SKILLS/EVIDENCE.md` (append)

### GESTE-5 — Vérifier hash frais (Preuve Fraîche)
Relire le fichier EVIDENCE.md, recalculer le hash, vérifier correspondance.

## Règles d'or
- Interdiction d'auto-référence : hash SHA-256 du fichier SKILL.md ne doit PAS être dans son propre frontmatter
- Hash SHA-256 recalculé sur fichier actuel sur disque (Preuve Fraîche)
- EVIDENCE.md append-only, jamais écrasé
- Horodatage UTC frais à chaque entrée

## Preuve d'exécution
- Date/heure : 2026-11-23T23:00:00Z
- WAL: 0x243
- IntentHash: 0xM3_SKILL_EVIDENCE_AUTO_ENROLLER_20261123

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Script principal | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skill-evidence-auto-enroller\evidence_enroller.py` |
| EVIDENCE.md global | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\EVIDENCE.md` |
| Config | `D:\DO\WEB\TOOLS\SKILLS\skill-evidence-auto-enroller\config.json` |

## Hash de ce skill
Horodatage: 2026-11-23T23:10:00Z | WAL: 0x243 | IntentHash: 0xM3_SKILL_EVIDENCE_AUTO_ENROLLER_20261123