
Feature: Creating a message

    Scenario: User creates a message
        Given User is on the create message page
        When User enters some text
        And User clicks the save button
        Then Message is stored in database
        And User is taken to message detail page