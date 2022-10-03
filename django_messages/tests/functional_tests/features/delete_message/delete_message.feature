Feature: Deleting a message

    Scenario: User deletes a message
        Given User is on the create message page
        When User visits the delete message page
        And User clicks the confirm button
        Then Message is deleted
        And User is taken to message list page