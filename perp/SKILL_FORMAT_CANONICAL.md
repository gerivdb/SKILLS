# Format Canonique des Skills Perplexity Spaces

> IntentHash : `0xPERPSKILLFORMAT_20260524`  
> Validé empiriquement — gerivdb/DEV_COMET ENV1  
> Statut : [CONFORME_NEXUS] — T2-OUTILS / L2-COMPOSITION

---

## Contexte

Le format des Skills Perplexity Spaces n'est pas documenté officiellement par Perplexity AI.  
Ce document est le résultat d'une validation empirique : comparaison de fichiers acceptés vs refusés dans un Space Perplexity SaaS (ENV1).

---

## Règles absolues d'acceptation

1. **Front-matter YAML en position 0** — aucun caractère, aucune ligne vide avant `---`.
2. **`name` en kebab-case strict** — minuscules, tirets uniquement, pas d'espace ni d'underscore.
3. **`description` sur deux lignes** : phrase courte + `Use when user mentions` suivi des mots-clés entre guillemets doubles, indentés de 2 espaces.
4. **4 sections exactes dans l'ordre** :
   - `## Instructions` (liste numérotée)
   - `## Règles` (liste à tirets)
   - `## Format` (liste à tirets)
   - `## Exemples` (liste à tirets)
5. **Aucune sous-section `###`**, aucun tableau dans le corps.
6. **Exactement 1 exemple** par skill, entre crochets `[...]` suivi d'une flèche `→`.
7. **Encodage UTF-8 sans BOM** obligatoire.
8. **ZIP à plat** lors de l'import : les fichiers `.md` doivent être à la racine du ZIP, pas dans un sous-dossier.

---

## Template canonique

```markdown
---
name: nom-du-skill
description: Description courte du rôle. Use when user mentions
  "mot-clé1", "mot-clé2", "mot-clé3".
---

# Titre Lisible du Skill

## Instructions

1. **Identifier la demande** : contexte et périmètre.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `<dépôt concerné>`.
3. **Appliquer les tags NEXUS**.
4. **Répondre en français**.

## Règles

- Règle canonique 1.
- Règle canonique 2.
- Ne pas inventer de commandes ou endpoints sans preuve.

## Format

- Format de sortie 1.
- Format de sortie 2.

## Exemples

- "[Déclencheur utilisateur typique]" → Action concrète.
```

---

## Exemples validés

| Fichier | Statut | Notes |
|---------|--------|-------|
| `perp/examples/ecosystem-maestro.md` | ✅ Accepté | Référence canonique |
| `perp/examples/brain-cortex.md` | ✅ Accepté | Référence canonique |
| `SKILL.md` (ancienne version) | ❌ Refusé | Cause probable : `description` sans `Use when user mentions` |

---

## Script de génération

Voir `perp/scripts/generate-skills.ps1` pour la génération automatique d'un ZIP de skills conforme.
