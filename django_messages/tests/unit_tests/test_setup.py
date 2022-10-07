import pytest
import redis
from contextlib import contextmanager
from django_q import tasks

"""
These will only pass if the ansible playbook has been run ie..

ansible-playbook django_messages/testapp/ansible_setup_test.yml
&& python -m pytest
&& ansible-playbook django_messages/testapp/ansible_teardown_test.yml

"""


# https://stackoverflow.com/a/42327075
@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("DID RAISE {0}".format(exception))


def test_redis_connection():
    r = redis.Redis(host="localhost", port=6379, db=1)
    with not_raises(ConnectionRefusedError):
        assert r.ping() == True


def test_django_q():
    brkr = tasks.get_broker()
    with not_raises(ConnectionRefusedError):
        assert brkr.ping() == True
