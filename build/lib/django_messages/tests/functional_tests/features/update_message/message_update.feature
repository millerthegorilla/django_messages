Feature: Update a message

    Scenario: User updates a message
        Given A message exists
        When User visits the update message page
        And User edits the message text
        And User clicks the save button
        Then The updated message is saved
        And User is redirected to view message page