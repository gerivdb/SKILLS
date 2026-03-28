---
name: audit-trail
description: Skill for tracking and auditing financial transactions and operations
triggers:
  - audit
  - trail
  - tracking
  - finance
  - transactions
  - compliance
domain: finance
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - audit
  - trail
  - tracking
  - finance
  - transactions
  - compliance
  - banking
phi_weight: 0.005
audit_trail_required: true
rgpd_note: "Données financières sensibles (transactions, comptes). Conformité RGPD et réglementaire requise."
---

# Audit Trail — Traçabilité des Opérations Financières

## Description

Ce skill domaine assure la traçabilité complète des opérations financières. Il enregistre, horodate et sécurise toutes les transactions pour garantir la conformité réglementaire et faciliter les audits.

## Usage

```
Quand [audit financier] OU [traçabilité transactions] OU [conformité réglementaire]
→ Appliquer audit-trail pour:
  1. Enregistrer chaque opération avec horodatage
  2. Calculer les hashs d'intégrité
  3. Générer des rapports d'audit
  4. Détecter les anomalies
  5. Exporter pour conformité réglementaire
```

## Composants

### 1. AuditLogger

```python
class AuditLogger:
    """Logger principal pour les opérations financières"""
    
    def __init__(self, config: AuditConfig):
        self.config = config
        self.storage = AuditStorage(config.storage)
    
    def log_operation(self, operation: FinancialOperation) -> AuditEntry:
        """Enregistre une opération financière"""
```

### 2. IntegrityHasher

```python
def calculate_audit_hash(entry: AuditEntry) -> str:
    """Calcule un hash d'intégrité pour un audit entry"""
    # SHA256(entry + timestamp + previous_hash)
```

### 3. AnomalyDetector

```python
def detect_anomalies(entries: list[AuditEntry]) -> list[Anomaly]:
    """Détecte les anomalies dans les transactions"""
    # ML + règles métier
```

### 4. ComplianceReporter

```python
def generate_compliance_report(entries: list[AuditEntry]) -> Report:
    """Génère un rapport de conformité"""
    # Format réglementaire (MiFID, RGPD, etc.)
```

## BIZ Domains

- **BIZ-2 (BANK-BUSTER)**: Usage principal pour l'audit des transactions bancaires
- **BIZ-1 (CANDIDATOR)**: Traçabilité des opérations de recrutement

## Exemples

### Exemple 1: Audit Transaction Bancaire

**Input:**
```python
logger = AuditLogger(config)

operation = FinancialOperation(
    type="transfer",
    amount=1500.00,
    currency="EUR",
    from_account="FR76...",
    to_account="FR76...",
    timestamp=datetime.now()
)

entry = logger.log_operation(operation)
```

**Output:**
```json
{
  "id": "audit_20260327_143022",
  "operation_type": "transfer",
  "amount": 1500.00,
  "currency": "EUR",
  "timestamp": "2026-03-27T14:30:22Z",
  "integrity_hash": "a1b2c3d4...",
  "status": "recorded"
}
```

### Exemple 2: Rapport de Conformité

**Input:**
```python
reporter = ComplianceReporter(config)
report = reporter.generate_report(
    start_date="2026-01-01",
    end_date="2026-03-31",
    format="pdf"
)
```

**Output:**
```
Rapport de Conformité Q1 2026
- Transactions totales: 1,234
- Anomalies détectées: 3
- Conformité MiFID: 99.8%
- Export: compliance_q1_2026.pdf
```

## Dépendances

### Dépend de
- Aucun

### Requis par
- `finance` (domain)

## Intégration

### BANK-BUSTER
```python
from skills.audit_trail import AuditLogger, AuditConfig

config = AuditConfig(
    storage="postgresql",
    retention_days=2555  # 7 ans
)
logger = AuditLogger(config)
```

## Configuration

```yaml
audit_trail:
  storage:
    type: postgresql
    connection: "${AUDIT_DB_URL}"
    retention_days: 2555
  
  hashing:
    algorithm: sha256
    chain_hash: true
  
  compliance:
    mifid: true
    rgpd: true
    export_formats: [pdf, json, csv]
  
  anomaly_detection:
    enabled: true
    threshold: 0.95
```

## Métriques

- **Temps d'enregistrement**: < 100ms
- **Intégrité**: 100% (hash chaîné)
- **Rétention**: 7 ans minimum
- **Conformité**: 99.9%

## Changelog

- 1.0.0 (2026-03-27) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
