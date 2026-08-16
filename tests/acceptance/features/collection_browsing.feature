Feature: Viewing a photography collection

  Scenario: Published photographs appear in their configured order
    Given a published collection contains published photographs
    When a visitor opens the collection
    Then the published photographs are displayed in their configured order
