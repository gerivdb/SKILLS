---
id: email-sender
label: Email Sender Skill
family: foundational
rank: F0
biz_domains: ["BIZ-RECRUIT", "BIZ-BOOKING", "BIZ-FINANCE"]
owner: BIZ-1
ref: ISI-20260328-EMAILSENDER
phi_weight: 0.005
rgpd_note: "Adresses email = données personnelles — consentement requis, opt-out obligatoire"
---

# EmailSenderSkill

Envoi d'emails transactionnels et de notifications via SMTP ou API (SendGrid, Resend).
Classifié **Foundational** : utilisé dans ≥3 domaines BIZ-* (RECRUIT + BOOKING + FINANCE).

## Usage

```python
from skills.foundational.email_sender import EmailSenderSkill
mailer = EmailSenderSkill(provider="resend")
mailer.send(to="candidate@example.com", template="interview_invite", context={...})
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `provider` | str | `smtp` \| `resend` \| `sendgrid` |
| `to` | str | Destinataire |
| `template` | str | Identifiant template |
| `context` | dict | Variables de rendu |

## Consommateurs

- `BIZ-RECRUIT` (owner) — invitations candidats, confirmations entretiens
- `BIZ-BOOKING` (consumer) — confirmations réservations, rappels
- `BIZ-FINANCE` (consumer) — alertes transactions, rapports

## Persona

`RecruteurBienveillant` : toujours inclure un lien de désinscription RGPD.
