---
id: template-render
label: Template Render Skill
family: domain
rank: D1
biz_domains: ["BIZ-RECRUIT", "BIZ-BOOKING"]
owner: BIZ-1
ref: ISI-20260328-TEMPLATERENDER
phi_weight: 0.005
rgpd_note: "Templates peuvent contenir des données personnelles — ne pas logger le rendu final"
---

# TemplateRenderSkill

Rendu de templates Jinja2/Markdown avec injection de variables contextuelles.
Classifié **Domain** (BIZ-RECRUIT + BIZ-BOOKING = 2 domaines, < 3 → Domain).
Requalifier en Foundational si BIZ-MEDIA confirme l'usage.

## Usage

```python
from skills.domain.recruitment.template_render import TemplateRenderSkill
renderer = TemplateRenderSkill(template_dir="templates/recruitment")
output = renderer.render("interview_invite.md.j2", context={"name": "Alice", "date": "2026-04-01"})
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `template_dir` | str | Répertoire des templates |
| `template` | str | Nom du fichier template |
| `context` | dict | Variables de rendu |

## Consommateurs

- `BIZ-RECRUIT` (owner) — emails candidats, lettres de mission
- `BIZ-BOOKING` (consumer) — confirmations, rappels

## Requalification trigger

Si `BIZ-MEDIA` (CLIP-FACTORY) utilise ce skill → monter en `native/foundational/template-render/`.
