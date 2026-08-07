Feature: Scaffold de skill
  En tant que skill-scaffold
  Je veux générer un skill conforme
  Afin de respecter les conventions de l'écosystème

  Scenario: Générer un skill avec structure TDD/BDD/ATDD/DDD/DbC/Hexagonal
    Given un nom de skill valide
    When je génère le scaffold
    Then la structure complète est créée
    And tous les tests templates sont présents
