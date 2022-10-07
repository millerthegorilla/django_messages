import pytest
import uuid
from django_messages import models as message_models

MESSAGE_TEXT = "Ipsum Lorum Dolum Est"


@pytest.fixture()
def test_message(db, message_text):
    try:
        message = message_models.Message.objects.get(text=message_text())
    except message_models.Message.DoesNotExist:
        message = message_models.Message.objects.create(text=message_text())
    return message


# used by unit tests, overriden in local conftest.py for functional tests
@pytest.fixture()
def message_text():
    def text():
        return str(uuid.uuid4().hex) + " : " + MESSAGE_TEXT

    return text
