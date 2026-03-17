---
name: booking
description: Orchestration des réservations et planification pour services
triggers:
  - booking
  - reservation
  - scheduling
  - calendar
  - rendez-vous
  - planification
domain: booking
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-17
updated: 2026-03-17
tags:
  - booking
  - scheduling
  - calendar
  - reservations
phi_weight: 0.005
deps:
  - product-context
---

# Booking — Orchestration Réservations

## Description

Ce skill domaine gère l'orchestration complète des réservations et de la planification pour les services. Il est utilisé par GERIBOOKING pour les réservations de services.

## Fonctionnalités

### 1. Availability Checker

```python
def check_availability(service_id: str, date_range: tuple) -> list[Slot]:
    """Vérifie les créneaux disponibles"""
    # Retourne liste de créneaux disponibles
```

### 2. Reservation Manager

```python
def create_reservation(
    customer: Customer,
    service: Service,
    slot: Slot,
    metadata: dict
) -> Reservation:
    """Crée une nouvelle réservation"""
    # Valide, crée, notifie
```

### 3. Calendar Integrator

```python
def sync_calendar(reservation: Reservation) -> SyncResult:
    """Synchronise avec les calendriers"""
```

## Usage

```
Quand [demande de réservation]
→ Vérifier disponibilité (check_availability)
→ Créer réservation (create_reservation)
→ Synchroniser calendrier (sync_calendar)
→ Confirmer client (send_confirmation)
```

## Exemples

### Exemple 1: Réservation Salon

**Input:**
```json
{
  "service": "Coiffure",
  "customer": {"email": "client@example.com"},
  "date": "2026-03-20",
  "duration": 60
}
```

**Process:**
1. Check: 2026-03-20 14:00 disponible
2. Create: Réservation #1234
3. Sync: Google Calendar updated
4. Confirm: Email envoyé

### Exemple 2: Réservation Multiple

**Input:**
```json
{
  "services": ["Massage", "Sauna"],
  "customer": {"email": "vip@example.com"},
  "date": "2026-03-21"
}
```

**Process:**
1. Check: Slots consécutifs disponibles
2. Create: Réservation groupée #1235
3. Package: Remise package appliquée

## Dépendances

### Dépend de
- `product-context` - Pour adapter le message de confirmation

### Requis par
- GERIBOOKING

## Intégration

### GERIBOOKING
```python
from skills.booking import (
    check_availability,
    create_reservation,
    sync_calendar
)

# Usage
slots = check_availability("coiffure", ("2026-03-20", "2026-03-21"))
reservation = create_reservation(customer, service, slot[0])
```

### FLUENCE (Confirmation Emails)
```python
from skills.booking import get_confirmation_template
from skills.product_context import adapt_message

template = get_confirmation_template(reservation)
email = adapt_message(template, customer.profile)
```

## Configuration

```yaml
booking:
  services:
    - id: coiffure
      name: Coiffure
      duration: 60
      slots: [9, 10, 11, 14, 15, 16, 17]
    - id: massage
      name: Massage
      duration: 90
      slots: [10, 14, 15]
  
  sync:
    google_calendar: true
    outlook: true
  
  notifications:
    email: true
    sms: false
```

## Changelog

- 1.0.0 (2026-03-17) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
