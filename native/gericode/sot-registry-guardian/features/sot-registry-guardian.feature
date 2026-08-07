Feature: Gardien du registre SOT
  En tant que sot-registry-guardian
  Je veux valider les chemins et métadonnées des repos
  Afin de garantir la cohérence de known_repositories.yaml

  Scenario: Détecter un mismatch local_path ↔ full_name
    Given known_repositories.yaml avec un repo valide
    When le local_path diffère du remote
    Then une erreur de validation est remontée
    And le rapport de drift est généré

  Scenario: Rejeter un repo hors strate L*
    Given un chemin `D:\DO\WEB\TOOLS\BAD`
    When je valide la strate
    Then `ValueError` est levé
    And le repo est marqué INVALIDE
