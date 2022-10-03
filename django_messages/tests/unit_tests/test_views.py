import ast
import pytest
from django_q.models import Schedule
from django_messages import models as message_models

ALLOWED_TEXT = '<h1 color="red" style="font-family: times;">bob me baby</h1>'
DISALLOWED_TEXT = '<script>evil script</script><disallowed_tag style="word-break: normal"></disallowed_tag><span style="font-size: 3em; word-break: normal">bob</span>'  # noqa: E501

ALLOWED_TEXT_POST_SANITIZE = ALLOWED_TEXT
DISALLOWED_TEXT_POST_SANITIZE = 'evil script<span style="font-size: 3em;">bob</span>'

NUM_OF_MESSAGES = 7


@pytest.fixture()
def test_message(db, message_text):
    def new_message(num_of_messages):
        for x in range(num_of_messages):
            message_models.Message.objects.create(text=message_text())
        return message_models.Message.objects.all()

    return new_message


def test_text_is_sanitized():
    assert ALLOWED_TEXT_POST_SANITIZE == message_models.Message.sanitize_text(
        ALLOWED_TEXT
    )
    assert DISALLOWED_TEXT_POST_SANITIZE == message_models.Message.sanitize_text(
        DISALLOWED_TEXT
    )


def test_message_list(test_message, client):
    test_message(NUM_OF_MESSAGES)
    response = client.get("/messages/")
    assert response.templates[0].name == "django_messages/message_list.html"
    assert response.context["page_obj"].number == 1
    assert response.context["page_obj"].paginator.num_pages == 2
    assert response.context["page_obj"].paginator.count == 7


def test_message_view(test_message, client):
    message = test_message(1)[0]
    response = client.get(f"/{message.id}/{message.slug}/")
    assert response.context["message"].text == message.text
    assert response.template_name[0] == "django_messages/message_detail.html"


@pytest.mark.locutus
def test_message_delete(db, client, test_message):
    message = test_message(1)[0]
    response = client.get(f"/delete_message/{message.id}/{message.slug}/")
    assert "Are you sure you want to delete" in response.content.decode()
    response = client.post(f"/delete_message/{message.id}/{message.slug}/")
    assert message_models.Message.objects.all().count() == 0
    assert response.url == "/messages/"
    message_models.Message.objects.alive_only = False
    assert message_models.Message.objects.all().count() == 1
    message_models.Message.objects.alive_only = True
    assert Schedule.objects.all().count() == 1
    assert (
        Schedule.objects.all().first().func
        == "django_messages.tasks.schedule_hard_delete"
    )
    assert (
        ast.literal_eval(Schedule.objects.all().first().kwargs)["text"]
        == message.text + " by " + message.author
        if message.author
        else "anonymous"
    )


def test_message_create(db, client, message_text):
    message_t = message_text()
    response = client.post("/create_message/", {"text": message_t})
    message = message_models.Message.objects.first()
    assert message.text == message_t
    assert response.url == message.get_absolute_url()
