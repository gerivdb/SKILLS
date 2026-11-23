# Documentation officielle KiloCode — Référentiel ENV2

**Version** : 1.0.0  
**IntentHash** : 0xKILO_DOC_REF_20261123  
**Statut** : accepted  
**Phase** : 8 (T071 à T080)

---

## 1. Portail officiel

| Sujet | URL |
|-------|-----|
| Portail général | https://kilo.ai/docs |
| Modes personnalisés (Custom Modes) | https://kilo.ai/docs/customize/custom-modes |
| Compétences (Skills) | https://kilo.ai/docs/customize/skills |

---

## 2. Configuration des modes/agents

Les modes/agents KiloCode se définissent par des fichiers Markdown avec frontmatter YAML :

- **Emplacement local** : `C:\Users\GG\.config\kilo\agents\` (ou `.kilo/agents/`, `.kilo/agent/`, `~/.config/kilo/agent/`)
- **Format** : frontmatter YAML (`mode`, `description`, `options`, `permission`) + corps Markdown
- **Types** : `primary`, `subagent`, `all`
- **Règle de permissions** : `last-match-wins` (la dernière règle correspondante l'emporte)
- **Chargement** : scan des répertoires au démarrage, rechargement via `/reload` ou nouvelle session

### Fichiers locaux existants sur ENV2

| Fichier | Chemin | Mode | Description |
|---------|--------|------|-------------|
| architect.md | `C:\Users\GG\.config\kilo\agents\architect.md` | primary | Stress-test technique, plans d'implémentation |
| data.md | `C:\Users\GG\.config\kilo\agents\data.md` | primary | Analyse données, notebooks Jupyter |

---

## 3. kilo.jsonc

**Chemin** : `C:\Users\GG\.config\kilo\kilo.jsonc`

Sections principales :
- `version` : version de la config
- `env` : environnement (ENV3 sur ce poste, mirror ENV2)
- `shard` : identifiant du shard
- `rag` : configuration RAG (index, endpoint de recherche)
- `cdp` : configuration CDP (host, port 9222, profil Profile 2, exécutable Chromium)
- `governance` : known_repositories.yaml, ADR dir, hooks dir
- `skills` : mapping des skills (ex: chromium_profile_2 → chemin)
- `permission` : bash, external_directory (chemins autorisés)

---

## 4. Modes locaux ENV2 (conventions, pas natifs KiloCode)

Les modes **BDCP** et **FREE** ne sont pas des modes natifs documentés dans la doc officielle KiloCode. Ce sont des conventions locales ENV2, définies dans :

- `C:\Users\GG\.kilocode\rules\kilo-modes-bdcp-free.md`

### Protocole de basculement
Le basculement entre modes doit être **explicite** : déclaré, justifié, confirmé. Aucun basculement automatique n'est autorisé.

---

## 5. Points de vigilance

1. **BDCP et FREE** : conventions ENV2 uniquement, non confirmées comme mots-clés natifs dans la doc officielle KiloCode.
2. **Dossiers legacy** : `.kilocode/agents/` est encore supporté pour compatibilité ascendante.
3. **Interface Settings** : `Settings → Agent Behaviour → Agents` permet aussi la configuration via UI.
4. **Règle last-match-wins** : vérifier qu'aucune règle permissive en dernier n'annule une restriction critique.

---

## 6. Références

| Référence | Chemin / URL |
|-----------|-------------|
| Doc officielle KiloCode | https://kilo.ai/docs |
| Custom Modes | https://kilo.ai/docs/customize/custom-modes |
| Skills | https://kilo.ai/docs/customize/skills |
| kilo.jsonc | `C:\Users\GG\.config\kilo\kilo.jsonc` |
| Agents locaux | `C:\Users\GG\.config\kilo\agents\` |
| Règles modes BDCP/FREE | `C:\Users\GG\.kilocode\rules\kilo-modes-bdcp-free.md` |

---

**Màj requise si** : modification de kilo.jsonc, ajout/suppression d'agent, ou changement de convention BDCP/FREE.