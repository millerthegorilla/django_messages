from pytest_bdd import given, scenarios, then, when

from django_messages import models as message_models

scenarios("../create_message.feature")


@given("User is on the create message page", target_fixture="page")
def user_is_on_create_message_page(create_message_page):
    return create_message_page


@when("User enters some text")
def user_enters_some_text(page, message_text):
    page.type(".message-create-form-text", message_text())


@when("User clicks the save button")
def user_clicks_save_button(page, db):
    page.click('input[type="submit"]')


@then("Message is stored in database")
def message_is_stored_in_database(db, message_text):
    assert message_models.Message.objects.first().text == message_text()


@then("User is taken to message detail page")
def user_is_taken_to_message_detail_page(db, page):
    message_text = message_models.Message.objects.first().text
    assert "Message" in page.get_page_title()
    page.assert_text(message_text, selector="#textarea")
