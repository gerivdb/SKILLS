# CONTRIBUTING — Guide de Contribution

**Version** : 1.0.0 · **Date** : 2026-03-17

Merci de votre intérêt pour contribuer au registre SKILLS d'ecosystem-1. Ce guide explique comment soumettre des skills de qualité.

## 📋 Types de Contributions

### 1. Nouveau Skill Natif

Ajout d'un skill développé par gerivdb pour ecosystem-1.

### 2. Skill Externe Assimilé

Intégration d'un skill tiers dans ecosystem-1.

### 3. Amélioration Documentation

Corrections, enhancements de la documentation existante.

### 4. Outils de Validation

Scripts CI, validators, generators.

---

## ✅ Checklist Soumission Skill

Avant de soumettre une PR, vérifiez :

- [ ] Frontmatter YAML complet (voir modèle ci-dessous)
- [ ] Nom du skill unique (pas de doublon)
- [ ] Fichier nommé `SKILL.md`
- [ ] Chemin cohérent avec la taxonomie
- [ ] Description ≤200 caractères
- [ ] Au moins 3 triggers définis
- [ ] Validateur local passé (`tools/validate-skills.sh`)
- [ ] REGISTRY.yaml mis à jour

---

## 📝 Modèle SKILL.md

```yaml
---
name: my-skill
description: Description courte et claire du skill
triggers:
  - trigger-1
  - trigger-2
  - trigger-3
domain: foundational|domain|external
version: "1.0.0"
author: gerivdb|external-username
license: MIT|Apache-2.0|BSD|...
status: active|deprecated|draft
created: 2026-03-17
updated: 2026-03-17
tags:
  - tag1
  - tag2
deps:
  - skill-dependency
phi_weight: 0.001
---

# My Skill

## Description

Description détaillée du skill...

## Usage

```markdown
Quand [condition de trigger], appliquer [action]...
```

## Exemples

### Exemple 1

[Description de l'exemple]

## Dependencies

- Dépend vers : [skill-1], [skill-2]
- Requis par : [consumer-1]

## Changelog

- 1.0.0 (2026-03-17) - Version initiale
```

---

## 🔧 Processus de Submission

### Étape 1: Préparation

```bash
# Cloner le dépôt
git clone https://github.com/gerivdb/SKILLS.git
cd SKILLS

# Créer une branche
git checkout -b feat/skills-[nom-du-skill]
```

### Étape 2: Créer le Fichier

Suivez le modèle ci-dessus et créez :

```
native/[foundational|domain]/[skill-name]/SKILL.md
```

### Étape 3: Validation Locale

```bash
# Rendre le script exécutable
chmod +x tools/validate-skills.sh

# Exécuter la validation
./tools/validate-skills.sh
```

### Étape 4: Mettre à jour REGISTRY.yaml

Ajoutez votre skill dans la section `skills:` du fichier.

### Étape 5: Commit & Push

```bash
git add .
git commit -m "feat(skills): add [skill-name] skill

- Add SKILL.md with frontmatter
- Update REGISTRY.yaml
- Add validation"

git push origin feat/skills-[nom-du-skill]
```

### Étape 6: Pull Request

Créez une PR avec le template `.github/PULL_REQUEST_TEMPLATE.md`.

---

## 🎯 Règles de Nommage

| Règle | Convention | Exemple |
|-------|------------|---------|
| Nom du skill | kebab-case | `product-context` |
| Fichier | SKILL.md | `SKILL.md` |
| Répertoire | kebab-case | `product-context/` |
| Branche | feat/skills-{name} | `feat/skills-booking` |

---

## 🔒 Gardes de Sécurité

### Interdit

- ❌ Modifier le contenu d'un submodule externe
- ❌ Ajouter un skill sans frontmatter
- ❌ Dupliquer un skill existant
- ❌ Modifier le chemin d'un skill sans migration

### Restrictions

- ⚠️ Modifier `REGISTRY.yaml` = approval requise
- ⚠️ Modifier `.gitmodules` = approval L3 requise
- ⚠️ Modifier `CITIZENS.md` = approval governance requise

---

## 🧪 Validation CI

### Checks Obligatoires

1. **YAML Frontmatter** : Vérifie la présence et la validité du frontmatter
2. **Liens** : Vérifie qu'aucun lien n'est cassé
3. **Doublons** : Vérifie qu'il n'y a pas de skills en double
4. **Schema** : Vérifie la conformité du REGISTRY.yaml

### Comment Trigger la CI

```bash
# Push sur une branche triggers automatiquement la CI
git push origin feat/skills-[nom]
```

### Échec CI

En cas d'échec :

1. Lire les logs d'erreur
2. Corriger les problèmes
3. Commiter les corrections
4. Pusher à nouveau

---

## 📜 License

En contribuant, vous acceptez que votre contribution soit sous licence MIT (sauf indication contraire).

---

## ❓ Support

- **Issues** : Ouvrir une issue pour bug ou question
- **Discussions** : Utiliser les GitHub Discussions
- **Slack** : #skills-registry sur ecosystem-1

---

*Merci de contribuer à ecosystem-1 !*
