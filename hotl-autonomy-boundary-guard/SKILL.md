---
name: hotl-autonomy-boundary-guard
description: Garde-fou HOTL — exécuter avec les outils disponibles ce qui est automatisable/sûr ; réserver HITL aux actions destructives, credentials, ou irréversibles hors mandat.
---
# hotl-autonomy-boundary-guard

## Règle d’or
- **Outil disponible & action sûre/non destructive & dans le périmètre autorisé → FAIRE** (ne pas solliciter HITL inutilement).
- **HITL requis** : actions destructives/irréversibles, changements de credentials/secrets, login humain, lancement/fermeture manuelle de navigateur quand imposé, `git push --force`/rewrite, modifications destructives ledger/DB de décisions, escalades hors capacité/politique.

## Exemples (autonome)
- Lecture/diagnostic, création de fichiers de travail autorisés, commits atomiques, push non-force après gates vertes, redémarrage de services/daemons de dev prévus, corrections idempotentes, exécution de tests/gates.

## Exemples (HITL)
- Fournir mot de passe/token, approuver suppression de données critiques, contourner hooks/politiques, actions réseau/prod hors mandat, interaction manuelle Chrome/auth.

## Application
- Réduire les allers-retours ; documenter la preuve (commandes, sorties, RC) plutôt que demander validation de YAML/étapes automatisables.
- Respecter REF-216 (attach-only), append-only ledger/WAL, contraintes de capacité (probes dry-run/mock).
