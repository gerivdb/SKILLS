# CAPTA Safety Protocol — Protocoles de Sécurité Scénique

## Description

Protocoles de garde-fou pour systèmes câblés sous tension — limites, arrêts d'urgence, seuils de sécurité. Ce skill définit les règles de sécurité physique pour CAPTA-4D.

## Quand l'utilisateur

- Mentionne "sécurité", "tension", "limite", "seuil", "arrêt d'urgence", "safety"
- Dépassement de seuils détecté par SafetyGuard
- Configuration de nouveaux seuils de sécurité
- Audit de sécurité d'une scène

## Niveaux de sécurité

| Niveau | Condition | Action |
|--------|-----------|--------|
| **NORMAL** | tension ∈ [t_min, t_max] | Opération standard |
| **WARNING** | tension > 0.8 * t_max | Alerte + log |
| **CRITICAL** | tension > t_max | Arrêt immédiat |
| **EMERGENCY** | rupture détectée | Arrêt d'urgence + rollback |

## Configuration des seuils

```yaml
# config/harm_thresholds.yaml
safety:
  t_min: 10.0      # Newtons — tension minimale (câble détendu)
  t_max: 5000.0    # Newtons — tension maximale (câble rompu)
  emergency_stop: true
  zones:
    - name: workspace
      x_min: 500, x_max: 9500
      y_min: 500, y_max: 9500
      z_min: 500, z_max: 5500
```

## Procédures d'urgence

1. **Détection dépassement** → SafetyGuard.check() retourne False
2. **Arrêt immédiat** → Orchestrator.reset()
3. **Log WAL** → Événement de sécurité journalisé
4. **Notification** → Alerte si mode monitoring actif

## Invariants de sécurité

- Aucune opération ne peut dépasser t_max sans validation HITL
- Les zones de sécurité sont vérifiées avant tout mouvement
- Le safety monitor est toujours actif (pas de mode "sans sécurité")

## Références

- Code: `gerivdb/CAPTA-4D/src/capta4d/core/safety.py`
- Config: `gerivdb/CAPTA-4D/config/harm_thresholds.yaml`
- Tests: `gerivdb/CAPTA-4D/tests/test_safety.py`
