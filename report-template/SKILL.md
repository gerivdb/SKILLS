---
name: report-template
description: Template obligatoire pour tout rapport d'ingénierie, PRD, ADR ou INTENT. Garantit la présence des sections AUDIT, DESIGN, PROPOSITION, VALIDATION. Utiliser avant de rédiger tout document technique.
version: 1.0.0
intent_hash: 0xREPORT_TEMPLATE_SKILL_20260809
---

# Report Template — Skill KiloCode

## Objectif

Forcer la structure **AUDIT → DESIGN → PROPOSITION → VALIDATION** pour tout document d'ingénierie.
Évite les documents qui sautent directement à la proposition sans état des lieux.

## Déclencheur

Avant toute rédaction de :
- Rapport d'ingénierie
- PRD / MOC
- ADR
- INTENT
- Design document
- Post-mortem

## Template Obligatoire

```markdown
# [TITRE]

**VERSION** : X.Y | **DATE** : YYYY-MM-DD | **INTENT HASH** : 0x...

---

## SOMMAIRE EXÉCUTIF

[Résumé en 5-10 lignes du problème, de la solution, et du statut]

---

## 1. AUDIT — ÉTAT DES LIEUX

### 1.1 Composants Existants

| Composant | Existence | État | Source |
|-----------|-----------|------|--------|
| [nom] | ✅/❌/⚠️ | [description] | `known_repositories.yaml` / repo local |

### 1.2 Contraintes Identifiées

| Contrainte | Type | Impact |
|------------|------|--------|
| [contrainte] | hardware/budget/temps/architecture | [description] |

### 1.3 Besoins Identifiés

| Besoin | Priorité | Source |
|--------|----------|--------|
| [besoin] | high/medium/low | PRD/ADR/issue/manuel |

---

## 2. DESIGN — CADRAGE

### 2.1 Critères de Sélection

| Critère | Poids | Justification |
|---------|-------|---------------|
| [critère] | 1-10 | [pourquoi ce critère] |

### 2.2 Options Évaluées

| Option | Avantages | Inconvénients | Score |
|--------|-----------|---------------|-------|
| [option A] | ... | ... | X/10 |
| [option B] | ... | ... | Y/10 |

### 2.3 Décision de Design

**Option retenue** : [nom]
**Justification** : [pourquoi cette option]
**Sources** : [références]

---

## 3. PROPOSITION — SOLUTION

### 3.1 Architecture

[Diagramme ASCII ou description textuelle]

### 3.2 Composants

| Composant | Rôle | Responsable |
|-----------|------|-------------|
| [nom] | [rôle] | [équipe/agent] |

### 3.3 Spécifications

| Élément | Spécification |
|---------|---------------|
| [entrée/sortie] | [format, contrainte] |
| [performance] | [métrique + seuil] |

### 3.4 Planning

| Phase | Actions | Durée | Dépendances |
|-------|---------|-------|-------------|
| [nom] | ... | ... | ... |

---

## 4. VALIDATION — PREUVES

### 4.1 Checklist de Validation

- [ ] Audit des repos existants complété
- [ ] Besoins documentés avec sources
- [ ] Critères de sélection définis
- [ ] Spécifications des modules documentées
- [ ] Indicateurs mesurables définis
- [ ] Tests unitaires prévus
- [ ] Tests E2E prévus
- [ ] Contraintes hardware vérifiées

### 4.2 Métriques de Validation

| Métrique | Cible | Mesure | Résultat |
|----------|-------|--------|----------|
| [métrique] | [cible] | [comment] | [valeurs] |

### 4.3 Preuves

| Preuve | Type | Fichier/Ref |
|--------|------|-------------|
| [preuve] | benchmark/test/issue | [chemin] |

---

## 5. CONCLUSION

| Point | Statut |
|-------|--------|
| [aspect] | ✅/⚠️/❌ |

**STATUT FINAL** : [prêt / bloqué / en attente]

**Actions requises** :
1. [action 1]
2. [action 2]
```

## Règles d'Utilisation

1. **Toujours commencer par l'AUDIT** — Ne pas sauter cette section
2. **Toujours lier à une source** — Chaque besoin, critère, composant doit avoir une référence
3. **Toujours définir des indicateurs** — Pas de métrique vague ("performant") — utiliser des seuils
4. **Toujours inclure la checklist** — La section 4.1 est obligatoire

## Exemple d'Application

**Mauvais** :
```markdown
# Rapport V9.10
## Conclusion
On implémente 113 effets After Effects.
```

**Bon** :
```markdown
# Rapport V9.10-R2
## 1. AUDIT
KORX existe, fait du .kbin, pas d'effets AE.
## 2. DESIGN
Critères: ENV2 compatibility, performance <100ms, 20 effets max.
## 3. PROPOSITION
20 effets core: 10 OpenCV, 5 FFmpeg, 5 Librosa.
## 4. VALIDATION
Checklist: [x] audit KORX, [x] benchmarks, [x] specs modules
```

## Anti-patterns

- ❌ Sauter l'audit et aller directement à la proposition
- ❌ Oublier les sources ("c'est une évidence")
- ❌ Oublier les indicateurs ("ça va être rapide")
- ❌ Oublier la checklist de validation

## Référence ADR

- **ADR** : ADR-2026-08-09-001-REPORT-TEMPLATE
- **IntentHash** : 0xREPORT_TEMPLATE_SKILL_20260809
- **Dépôt** : gerivdb/GeriCode
