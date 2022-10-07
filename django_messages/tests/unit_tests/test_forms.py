import pytest
from django_messages import forms as message_forms
from django_messages import models as message_models

ALLOWED_TEXT = '<h1 color="red" style="font-family: times;">bob me baby</h1>'
DISALLOWED_TEXT = '<script>evil script</script><disallowed_tag style="word-break: normal"></disallowed_tag><span style="font-size: 3em; word-break: normal">bob</span>'  # noqa: E501

ALLOWED_TEXT_POST_SANITIZE = ALLOWED_TEXT
DISALLOWED_TEXT_POST_SANITIZE = 'evil script<span style="font-size: 3em;">bob</span>'


def test_text_is_sanitized():
    assert ALLOWED_TEXT_POST_SANITIZE == message_forms.Message.sanitize_text(
        ALLOWED_TEXT
    )
    assert DISALLOWED_TEXT_POST_SANITIZE == message_forms.Message.sanitize_text(
        DISALLOWED_TEXT
    )


def test_form_with_data(test_message):
    form = message_forms.Message(test_message.__dict__)
    assert form["text"].value() == test_message.text


@pytest.mark.locutus
def test_form_sanitize_text(db):
    form = message_forms.Message({"text": DISALLOWED_TEXT})
    message = form.save()
    assert message.text == DISALLOWED_TEXT_POST_SANITIZE
