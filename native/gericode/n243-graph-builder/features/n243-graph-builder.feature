Feature: Construction du graphe N243
  En tant que n243-graph-builder
  Je veux construire un graphe de repos
  Afin de représenter les dépendances de l'écosystème

  Scenario: Construire un graphe à partir de known_repositories.yaml
    Given known_repositories.yaml valide
    When je construis le graphe N243
    Then le graphe contient tous les repos actifs
    And les bridges sont préservés

  Scenario: Détecter un cycle dans le graphe
    Given deux repos avec dépendance circulaire
    When je construis le graphe
    Then une exception est levée
    And le cycle est identifié
