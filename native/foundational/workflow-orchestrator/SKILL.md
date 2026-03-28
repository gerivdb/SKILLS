---
name: workflow-orchestrator
description: Skill for orchestrating daily automated workflows
triggers:
  - workflow
  - orchestration
  - automation
  - daily
  - process
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - workflow
  - orchestration
  - automation
  - daily
  - process
  - multi-step
phi_weight: 0.005
rgpd_note: "Données de workflow et informations personnelles. Conformité RGPD requise pour l'orchestration automatisée."
deps:
  - notion-connector
  - perplexity-sourcer
---

# Workflow Orchestrator — Orchestration de Workflows Automatisés

## Description

Ce skill fondamental orchestre les workflows automatisés quotidiens. Il fournit une interface unifiée pour exécuter des processus multi-étapes avec validation, assistance IA et capacités de sauvegarde automatique.

## Usage

```
Quand [exécution de workflow quotidien] OU [automatisation de processus multi-étapes]
→ Appliquer workflow-orchestrator pour:
  1. Configurer les étapes du workflow
  2. Exécuter avec suivi de progression
  3. Valider automatiquement à chaque étape
  4. Intégrer l'assistance IA (optionnel)
  5. Sauvegarder automatiquement les fichiers générés
```

## Composants

### 1. CANDIDATORWorkflow

```python
class CANDIDATORWorkflow:
    """Orchestrateur principal pour les workflows CANDIDATOR"""
    
    def __init__(self, config: WorkflowConfig):
        self.config = config
        self.notion_client = NotionIDEClient(config.notion)
        self.validator = CANDIDATORValidator()
        self.ai_analyzer = CursorAIAnalyzer() if config.enable_ai else None
    
    def run_complete_workflow(
        self,
        candidature_id: int,
        profil: str,
        auto_copy: bool = True
    ) -> WorkflowResult:
        """Exécute le workflow complet"""
```

### 2. WorkflowConfig

```python
@dataclass
class WorkflowConfig:
    """Configuration du workflow"""
    auto_backup: bool = True
    enable_ai_assistance: bool = False
    validation_strict: bool = True
    output_format: str = 'markdown'
    backup_location: str = './backups'
```

### 3. StepExecutor

```python
class StepExecutor:
    """Exécuteur d'étapes individuelles"""
    
    def execute_step(self, step: WorkflowStep) -> StepResult:
        """Exécute une étape avec validation"""
        # Exécution + validation + logging
```

### 4. ProgressTracker

```python
class ProgressTracker:
    """Suivi de progression du workflow"""
    
    def update_progress(self, step: int, total: int, status: str):
        """Met à jour la progression"""
        # Affichage console + métriques
```

## BIZ Domains

- **BIZ-1 (CANDIDATOR)**: Usage principal pour l'orchestration du workflow de génération de CV
- **BIZ-2 (BANK-BUSTER)**: Traitement potentiel de workflows de transactions financières
- **BIZ-3 (RACINES)**: Automatisation potentielle de workflows de recherche généalogique

## Exemples

### Exemple 1: Workflow Génération CV

**Input:**
```python
config = WorkflowConfig(
    auto_backup=True,
    enable_ai_assistance=True
)
workflow = CANDIDATORWorkflow(config)

result = workflow.run_complete_workflow(
    candidature_id=123,
    profil="mediateure-numerique",
    auto_copy=True
)
```

**Output:**
```
Workflow exécuté avec succès:
- Étape 1: Récupération données Notion ✓
- Étape 2: Génération CV markdown ✓
- Étape 3: Validation contenu ✓
- Étape 4: Analyse IA ✓
- Étape 5: Sauvegarde ✓
Fichier: CV_123_mediateure-numerique_20260327.md
```

### Exemple 2: Workflow Batch

**Input:**
```python
config = WorkflowConfig(auto_backup=True)
workflow = CANDIDATORWorkflow(config)

results = workflow.run_batch_workflow(
    candidature_ids=[101, 102, 103, 104, 105],
    profil="developpeur-python"
)
```

**Output:**
```
Batch workflow terminé:
- 5 candidatures traitées
- 5 CV générés
- 0 erreur
Temps total: 45.2s
```

## Dépendances

### Dépend de
- `notion-connector` - Pour récupération des données
- `perplexity-sourcer` - Pour sourcing d'offres (optionnel)

### Requis par
- `recruitment` (domain)

## Intégration

### CANDIDATOR
```python
from skills.workflow_orchestrator import CANDIDATORWorkflow, WorkflowConfig

config = WorkflowConfig(
    auto_backup=True,
    enable_ai_assistance=True
)
workflow = CANDIDATORWorkflow(config)
result = workflow.run_complete_workflow(123, "developpeur-python")
```

### VS Code / Cursor
```python
# Mode interactif pour IDE
from skills.workflow_orchestrator import InteractiveWorkflow

interactive = InteractiveWorkflow()
interactive.run_interactive_mode()
```

## Configuration

```yaml
workflow:
  steps:
    - name: data-retrieval
      source: notion-connector
      required: true
    
    - name: content-generation
      template: cv-template.md
      required: true
    
    - name: validation
      strict: true
      required: true
    
    - name: ai-analysis
      enabled: false
      required: false
    
    - name: backup
      location: ./backups
      required: true
  
  execution:
    timeout: 300
    retry_attempts: 3
    parallel: false
  
  logging:
    level: INFO
    file: ./logs/workflow.log
    metrics: true
```

## Métriques

- **Temps d'exécution**: < 10s pour workflow simple
- **Temps batch**: < 5s par candidature
- **Taux de succès**: 99.5%
- **Sauvegarde**: 100% des fichiers générés

## Changelog

- 1.0.0 (2026-03-27) - Version initiale extraite de CANDIDATOR

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
