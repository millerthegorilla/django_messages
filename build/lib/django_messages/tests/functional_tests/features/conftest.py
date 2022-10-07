import pytest
import os
from django.urls import reverse
from django_messages import models as message_models

MESSAGE_TEXT = "Ipsum Lorum Dolum Est"

CREATE_MESSAGE_URL = reverse("django_messages:message_create")
LIST_MESSAGE_URL = reverse("django_messages:message_list")

LINKS_DICT = {
    "create_message": f"a[href='{CREATE_MESSAGE_URL}']",
    "list_message": f"a[href='{LIST_MESSAGE_URL}']",
}

PAGES_DICT = {
    "create_message": CREATE_MESSAGE_URL,
    "list_message": LIST_MESSAGE_URL,
}


@pytest.fixture()
def message_text():
    return lambda: MESSAGE_TEXT


@pytest.fixture()
def browser(sb, live_server, settings):
    staging_server = os.environ.get("STAGING_SERVER", False)
    if staging_server:
        sb.visit(staging_server)
    else:
        sb.visit(live_server)
    sb.domain = sb.get_domain_url(sb.get_current_url())
    settings.EMAIL_PAGE_DOMAIN = sb.domain
    sb.pages = PAGES_DICT
    sb.links = LINKS_DICT
    return sb


@pytest.fixture()
def create_message_page(browser):
    browser.visit(browser.domain + CREATE_MESSAGE_URL)
    return browser
