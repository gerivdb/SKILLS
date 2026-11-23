# Table de correspondance des modes KiloCode — ENV2

**Version** : 1.0.0  
**Horodatage UTC** : 2026-11-23T05:55:00Z  
**Source** : D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json

## 1. Table de correspondance mode → profil → classe

Ce document élimine les alias ambigus entre modes KiloCode natifs, profils locaux BDCP/FREE et préfixes de classe (m3-).

| mode_id | kind | vocation | write_policy | lease_required | config_path | alias/préfixe | classe d'usage |
|---------|------|----------|--------------|----------------|-------------|---------------|----------------|
| architect | agent_definition | audit | read_only | false | C:\Users\GG\.config\kilo\agents\architect.md | m3-audit, audit-mode | Agent d'analyse et de cadrage (lecture seule) |
| data | agent_definition | execution | lease_required | true | C:\Users\GG\.config\kilo\agents\data.md | m3-exec, exec-mode | Agent d'exécution (écriture conditionnée par bail) |
| bdcp | rule_profile | diagnostic | read_only | false | C:\Users\GG\.kilocode\rules\kilo-modes-bdcp-free.md | bdcp-mode, clapet-fermé | Profil CDP local, port 9222, clapet fermé |
| free | rule_profile | lecture | read_only | false | C:\Users\GG\.kilocode\rules\kilo-modes-bdcp-free.md | free-mode, econome | Profil sans abonnement, sobriété de contexte |

## 2. Règles de désambiguïsation

- **agent_definition** : correspond à un fichier agent dans `C:\Users\GG\.config\kilo\agents\` (format KiloCode natif avec frontmatter `mode`, `options`, `permission`).
- **rule_profile** : correspond à un profil porté par une règle KiloCode dans `C:\Users\GG\.kilocode\rules\` (ici `kilo-modes-bdcp-free.md`).
- **BDCP** n'est pas un mot-clé natif de la documentation officielle KiloCode ; c'est une convention locale ENV2 (Behind CDP).
- **FREE** n'est pas un mot-clé natif de la documentation officielle KiloCode ; c'est une convention locale ENV2 (sobriété, zéro abonnement payant).
- Le préfixe `m3-` est réservé aux classifications internes du modèle M3 (M3TREE, m3-intent-latch, etc.) et ne doit pas être confondu avec un mode KiloCode.

## 3. Conditions d'entrée et de sortie par mode (T104)

### architect (agent_definition, audit, read_only)
**Entrée** :
- permissions read allow
- permissions edit deny (sauf plans)
- permissions bash deny
- permissions mcp deny
- territoire : aucun bail requis (mode lecture)

**Sortie** :
- plan écrit dans `.kilo/plans/` ou `.plans/`
- `plan_exit` appelé
- aucun fichier source modifié

### data (agent_definition, execution, lease_required)
**Entrée** :
- permissions read allow
- permissions edit allow
- permissions bash allow
- permissions mcp allow
- bail actif sur le territoire cible (via claim-lease.ps1)

**Sortie** :
- notebook cells appended and executed
- notebook history preserved
- bail libéré ou transféré

### bdcp (rule_profile, diagnostic, read_only)
**Entrée** :
- clapet BDCP fermé par défaut
- port CDP 9222 accessible sur 127.0.0.1
- profil Chromium Profile 2 authentifié

**Sortie** :
- clapet BDCP reste fermé
- aucune sortie réseau directe
- profil temporaire non utilisé

### free (rule_profile, lecture, read_only)
**Entrée** :
- pas d'abonnement payant
- sobriété d'appels et de contexte
- chemins explicites obligatoires

**Sortie** :
- pas de basculement automatique vers BDCP
- aucun chemin par défaut substitutif

## 4. Preuve de validation

- modes-matrix.schema.json : Test-Path positif + validation JSON ($LASTEXITCODE -eq 0)
- modes-matrix.json : 4 modes, tous avec chemins de config existants sur disque
