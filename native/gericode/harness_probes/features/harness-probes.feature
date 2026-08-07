Feature: Harness probes execution
  As a harness operator
  I want to run probes P-701..P-711
  So that I can verify the GeriCode stack compliance

  Scenario: Run all probes
    When I run the harness probes
    Then I should see 11 probe results
    And all probes should pass
