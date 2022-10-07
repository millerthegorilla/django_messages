Feature: Listing messages

    Scenario: User lists all messages
        Given A message exists
        When User visits the message list page
        Then The message is listed