Feature: Injection YAML sécurisée
  En tant que skill yaml-safe-injector
  Je veux injecter des champs dans known_repositories.yaml
  Afin de ne pas corrompre la structure YAML

  Scenario: Injecter verse_mapping sans corrompre les ancres YAML
    Given un fichier YAML avec ancres `&id001`
    When j'injecte `verse_mapping: verse` pour `VERSES`
    Then la structure YAML est préservée
    And le diff est minimal

  Scenario: Rejeter un chemin hors strate L*
    Given un chemin `D:\DO\WEB\TOOLS\BAD`
    When j'appelle `inject_yaml` avec ce chemin
    Then l'erreur `ValueError` est levée
    And le fichier n'est pas modifié
