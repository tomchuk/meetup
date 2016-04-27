Feature: Creating a Todo
  As a user
  I want to create a Todo
  So that I can remember to buy milk

  Scenario: Create a todo
    Given I am logged in via facebook
    When I visit the home page
    And I fill out the todo name
    And I press enter
    Then I should see my todo