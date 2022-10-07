import pytest
import datetime
import redis
import ast
from freezegun import freeze_time

from django_q import tasks
from django_q.models import Schedule

from django import conf, urls
from django.core.management import call_command

from django_messages import models as message_models

from test_setup import not_raises
from test_forms import DISALLOWED_TEXT, DISALLOWED_TEXT_POST_SANITIZE

with freeze_time():
    NOW = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)


@freeze_time(NOW)
def test_message_created_at(db, message_text):
    msg = message_models.Message.objects.create(text=message_text())
    assert msg.created_at == NOW


@pytest.fixture()
def django_db_setup(settings, django_db_blocker):
    conf.settings.ABSTRACTMESSAGE = True
    with django_db_blocker.unblock():
        call_command("makemigrations")
        call_command("migrate", "--noinput")
    yield


@pytest.fixture()
def reset_schedules(db):
    Schedule.objects.all().delete()


def test_message_isnt_created_when_abstract(django_db_setup, db):
    with pytest.raises(AttributeError):
        message_models.Messages.objects.create(text=DISALLOWED_TEXT)


def test_absolute_url(test_message):
    assert test_message.get_absolute_url() == urls.reverse_lazy(
        "django_messages" + ":message_view", args=[test_message.id, test_message.slug]
    )


def test_model_delete(reset_schedules, test_message):
    test_message.delete()
    assert test_message.active == False
    brkr = tasks.get_broker()
    with not_raises(redis.exceptions.ConnectionError):
        assert brkr.ping() == True
    assert Schedule.objects.all().count() == 1
    assert (
        Schedule.objects.all().first().func
        == "django_messages.tasks.schedule_hard_delete"
    )
    assert (
        ast.literal_eval(Schedule.objects.all().first().kwargs)["text"]
        == test_message.text + " by " + test_message.author
        if test_message.author
        else "anonymous"
    )
