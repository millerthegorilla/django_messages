import pytest
import uuid

MESSAGE_TEXT = "Ipsum Lorum Dolum Est"


@pytest.fixture()
def message_text():
    def text():
        return str(uuid.uuid4().hex) + " : " + MESSAGE_TEXT

    return text
