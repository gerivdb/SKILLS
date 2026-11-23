# Séparation des modes KiloCode — Exploration/Diagnostic vs Mutation (T106)

**Version** : 1.0.0  
**Horodatage UTC** : 2026-11-23T06:00:00Z  
**Source** : D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json

## 1. Modes en lecture/exploration (read_only)

Ces modes ne modifient aucun fichier de production, aucun livrable, aucun script. Ils sont réservés à l'analyse, au diagnostic, à la lecture et au cadrage.

| mode_id | kind | vocation | write_policy | lease_required | Usage principal |
|---------|------|----------|--------------|----------------|-----------------|
| architect | agent_definition | audit | read_only | false | Stress-test technique, plans d'implémentation, cadrage |
| bdcp | rule_profile | diagnostic | read_only | false | Pilotage CDP sur port 9222, diagnostic, inspection |
| free | rule_profile | lecture | read_only | false | Sobriété de contexte, zéro abonnement, lecture seule |

**Règle** : Aucun de ces modes ne peut exécuter `git add/commit/push`, `Set-Content`, `New-Item` sur des fichiers de production, ni modifier `skills/`, `skill-bank/`, `.kilocode/rules/`, `.kilo/`.

---

## 2. Modes en écriture/mutation (lease_required)

Ces modes sont autorisés à modifier des fichiers, mais uniquement sous couvert d'un bail actif sur le territoire cible (via claim-lease.ps1).

| mode_id | kind | vocation | write_policy | lease_required | Usage principal |
|---------|------|----------|--------------|----------------|-----------------|
| data | agent_definition | execution | lease_required | true | Exécution de notebooks, écriture de scripts, mutation de code |

**Règle** : Toute écriture en mode `data` doit être précédée de l'acquisition d'un bail horodaté UTC sur le territoire cible. Sans bail, l'écriture est bloquée.

---

## 3. Hiérarchie des sous-agents et délégations task (T107)

### Principe
Un mode principal (ex: architect en mode audit) peut déléguer à un sous-agent (subagent) ou via la commande `task` uniquement lorsque :
1. La sous-tâche est atomique (1 fichier, 1 question, 1 réponse)
2. Le sous-agent opère dans un mode compatible (lecture si le mode principal est lecture, écriture si le mode principal a un bail actif)
3. Le délégueur conserve la responsabilité du résultat

### Règle de délégation
- **Déléguer** si le sous-problème est atomique et peut être décrit en une phrase simple
- **Ne pas déléguer** si le sous-problème nécessite lui-même une fragmentation ou une décision architecturale
- Un sous-agent ne doit jamais créer lui-même des sub-agents (pas de délégation en cascade)

### Tableau de délégation

| Mode principal | Peut déléguer à | Conditions |
|----------------|------------------|------------|
| architect | subagent lecture | Tâche d'analyse atomique, pas de mutation |
| data | subagent écriture | Bail actif sur le territoire, tâche atomique |
| bdcp | aucun | Mode diagnostic, pas de délégation |
| free | subagent lecture | Tâche de lecture atomique, pas de mutation |

---

## 4. Cas interdits par mode (anti-usages) (T109)

| mode_id | Action interdite | Raison |
|---------|-----------------|--------|
| architect | `git add/commit/push` sur fichiers de production | Mode audit, pas de mutation |
| architect | `Set-Content` sur `skills/`, `skill-bank/`, `.kilocode/rules/` | Mode lecture, écriture interdite |
| architect | Basculer vers mode `data` sans bail explicite | Élévation de droits interdite |
| data | Écrire sans bail actif sur le territoire | Garde-fou pré-écriture (mode-write-guard) |
| data | Ouvrir le clapet BDCP V1 | Furtivité réseau interdite |
| bdcp | `git add/commit/push` | Mode diagnostic, pas de mutation |
| bdcp | Ouvrir une nouvelle fenêtre Chromium | Toujours un nouvel onglet, jamais nouvelle fenêtre |
| free | `POST /clapet/open` | Ordre utilisateur explicite requis |
| free | Utiliser un chemin par défaut (ex: `D:\DO\WEB\TOOLS\SKILLS`) | Explicit Path Compliance |
| free | Basculer automatiquement vers un autre mode | Basculement explicite uniquement |

---

## 5. Preuve de validation

- modes-nomenclature.md : Test-Path positif + contenu cohérent avec modes-matrix.json
- 4 modes classés (3 read_only, 1 lease_required)
- 12 anti-usages documentés
