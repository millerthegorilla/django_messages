import pytest

from pytest_bdd import given, scenarios, then, when
from django_messages import models as message_models

scenarios("../message_detail.feature")


@given("A page", target_fixture="page")
def a_page(browser):
    return browser


@when("User visits the correct url")
def user_visits_the_correct_url(db, page, test_message):
    page.visit(page.domain + f"/{test_message.id}/{test_message.slug}")
    return page


@then("The message can be viewed")
def the_message_can_be_viewed(page, test_message):
    page.assert_text(test_message.text)
