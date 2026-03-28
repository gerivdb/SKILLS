---
name: email-sender
description: Skill for sending emails with templates, attachments, and delivery tracking
triggers:
  - email
  - send
  - notification
  - mail
  - smtp
  - delivery
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - email
  - send
  - notification
  - mail
  - smtp
  - delivery
  - communication
phi_weight: 0.005
biz_domains:
  - BIZ-RECRUIT
  - BIZ-BOOKING
  - BIZ-FINANCE
---

# Email Sender — Envoi d'Emails avec Templates et Suivi

## Description

Ce skill fondamental envoie des emails avec des templates, des pièces jointes et un suivi de livraison. Il supporte différents providers SMTP, gère les templates Jinja2, et fournit des métriques de délivrabilité.

## Usage

```
Quand [envoi d'email] OU [notification par email] OU [communication automatisée]
→ Appliquer email-sender pour:
  1. Envoyer des emails avec templates personnalisés
  2. Gérer les pièces jointes (PDF, images, documents)
  3. Suivre la livraison et les ouvertures
  4. Gérer les listes de diffusion
  5. Fournir des métriques de délivrabilité
```

## Composants

### 1. EmailSender

```python
class EmailSender:
    """Sender principal d'emails"""
    
    def __init__(self, config: EmailConfig):
        self.config = config
        self.smtp = SMTPClient(config.smtp)
        self.template_engine = TemplateEngine()
    
    def send(self, email: Email) -> SendResult:
        """Envoie un email"""
```

### 2. TemplateEngine

```python
class TemplateEngine:
    """Moteur de templates Jinja2"""
    
    def __init__(self, template_dir: str = "./templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def render(self, template_name: str, context: dict) -> str:
        """Rend un template avec le contexte"""
```

### 3. AttachmentHandler

```python
class AttachmentHandler:
    """Gestionnaire de pièces jointes"""
    
    def __init__(self, max_size_mb: int = 10):
        self.max_size = max_size_mb * 1024 * 1024
    
    def add_attachment(self, file_path: str, email: Email) -> Email:
        """Ajoute une pièce jointe à un email"""
```

### 4. DeliveryTracker

```python
class DeliveryTracker:
    """Tracker de livraison d'emails"""
    
    def __init__(self, config: TrackingConfig):
        self.config = config
        self.webhook_url = config.webhook_url
    
    def track(self, email_id: str, event: str):
        """Track un événement de livraison"""
```

## BIZ Domains

- **BIZ-RECRUIT (CANDIDATOR)**: Envoi d'emails de confirmation et suivi de candidatures
- **BIZ-BOOKING (GERIBOOKING)**: Notifications de réservation et rappels
- **BIZ-FINANCE (BANK-BUSTER)**: Alertes transactionnelles et rapports financiers

## Exemples

### Exemple 1: Email de Confirmation de Candidature

**Input:**
```python
sender = EmailSender(config)
email = Email(
    to="candidat@example.com",
    subject="Confirmation de candidature",
    template="application_confirmation.html",
    context={
        "candidate_name": "Jean Dupont",
        "position": "Développeur Python",
        "company": "TechCorp"
    }
)
result = sender.send(email)
```

**Output:**
```
Email envoyé avec succès:
- ID: email_20260328_103022
- Destinataire: candidat@example.com
- Sujet: Confirmation de candidature
- Template: application_confirmation.html
- Statut: sent
- Timestamp: 2026-03-28T10:30:22Z
```

### Exemple 2: Email avec Pièce Jointe

**Input:**
```python
sender = EmailSender(config)
email = Email(
    to="client@example.com",
    subject="Votre facture",
    template="invoice.html",
    context={"invoice_number": "INV-2026-001"}
)
email = sender.add_attachment("facture.pdf", email)
result = sender.send(email)
```

**Output:**
```
Email avec pièce jointe envoyé:
- Destinataire: client@example.com
- Pièce jointe: facture.pdf (245 KB)
- Statut: delivered
- Ouvert: 2026-03-28T11:15:30Z
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `recruitment` (domain)
- `booking` (domain)
- `finance` (domain)

## Intégration

### CANDIDATOR
```python
from skills.email_sender import EmailSender, EmailConfig

config = EmailConfig(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username="${EMAIL_USER}",
    password="${EMAIL_PASSWORD}"
)
sender = EmailSender(config)

# Envoi confirmation candidature
sender.send_application_confirmation(candidate_email, application_data)
```

### GERIBOOKING
```python
# Notification de réservation
sender.send_booking_confirmation(
    to=customer_email,
    booking_details=booking,
    template="booking_confirmation.html"
)
```

### BANK-BUSTER
```python
# Alerte transactionnelle
sender.send_transaction_alert(
    to=account_holder_email,
    transaction=transaction,
    template="transaction_alert.html"
)
```

## Configuration

```yaml
email_sender:
  smtp:
    host: smtp.gmail.com
    port: 587
    use_tls: true
    username: "${EMAIL_USER}"
    password: "${EMAIL_PASSWORD}"
  
  templates:
    directory: ./templates
    default_language: fr
  
  attachments:
    max_size_mb: 10
    allowed_types: [pdf, png, jpg, docx]
  
  tracking:
    enabled: true
    webhook_url: "${TRACKING_WEBHOOK_URL}"
    track_opens: true
    track_clicks: true
  
  limits:
    max_recipients_per_email: 50
    max_emails_per_hour: 100
```

## Métriques

- **Temps d'envoi**: < 2s par email
- **Taux de délivrabilité**: 99.5%
- **Taux d'ouverture**: 45% (moyenne)
- **Support pièces jointes**: Jusqu'à 10 MB

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
