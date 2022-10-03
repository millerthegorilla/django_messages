import pytest

from pytest_bdd import given, scenarios, then, when
from django_messages import models as message_models

scenarios("../delete_message.feature")


@given("User is on the create message page", target_fixture="page")
def user_is_on_create_message_page(create_message_page):
    return create_message_page


@when("User visits the delete message page")
def user_visits_delete_message_page(db, test_message, page):
    url = f"{page.domain}/delete_message/{test_message.id}/{test_message.slug}/"
    page.visit(url)
    return page


@when("User clicks the confirm button")
def user_clicks_confirm_button(page):
    page.click("input[type='submit']")


@then("Message is deleted")
def message_is_deleted(test_message):
    with pytest.raises(message_models.Message.DoesNotExist):
        message_models.Message.objects.get(id=test_message.id)


@then("User is taken to message list page")
def user_is_taken_to_message_list_page(page):
    assert "Message list" in page.get_page_title()
    assert "There are currently no messages." in page.get_page_source()
