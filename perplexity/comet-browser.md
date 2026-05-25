---
name: comet-browser
description: "COMET, BIRDY, headless browsers, CDP automation, browser extensions. Use when user mentions 'COMET', 'BIRDY', 'headless', 'CDP', 'navigateur IA'."
---
|
# Comet Browser

## Domaine et périmètre

Ce skill couvre l'automatisation de navigateurs via **COMET** et **BIRDY** :
- Navigation headless (sans interface graphique)
- Automatisation CDP (Chrome DevTools Protocol)
- Extensions de navigateur pour l'écosystème gerivdb
- Intégration avec le mode BDCP (Behind CDP) pour l'anonymat réseau

## Méthodologie

### Phase 1 : Configuration du navigateur
- Choisir le mode : headless (COMET) ou avec interface (BIRDY).
- Configurer le profil (user-agent, proxy BDCP, cookies).
- Vérifier la connectivité CDP (`http://localhost:9222`).

### Phase 2 : Automatisation
- Écrire le script de navigation (sélecteurs, actions, assertions).
- Gérer les attentes (wait for selector, wait for navigation).
- Capturer les screenshots et logs si nécessaire.

### Phase 3 : Extraction et livraison
- Extraire les données de la page (DOM, réseau, console).
- Formater les résultats selon le format de sortie.
- Nettoyer la session (fermeture, cookies, cache).

## Règles de décision
- **Règle 1** : Toujours utiliser le mode BDCP sauf ordre explicite de l'utilisateur.
- **Règle 2** : COMET pour les tâches automatisées, BIRDY pour le débogage visuel.
- **Règle 3** : Les sélecteurs CSS sont prioritaires sur XPath (plus stables).

## Format de sortie

```markdown
## Session COMET/BIRDY
- Mode : [headless | interface]
- Pages visitées : [N]
- Données extraites : [résumé]
- Screenshots : [chemins]
```

## Exemples d'utilisation
- "Scrape la page GitHub de gerivdb/NEXUS" → Automatiser et extraire.
- "Vérifie que le workflow IRIS est actif" → Naviguer et capturer.
- "Teste l'extension COMET sur le dépôt X" → Charger et valider.

## Intégration avec l'écosystème
- Dépôts concernés : COMET-BOT, BIRDY, GATEWAY-MANAGER
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS], [BDCP]
