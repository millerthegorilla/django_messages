# django_messages
a django app that provides basic message functionality, as a foundation for other apps.  It has a simple model from which other models can extend, or you can use django_messages on its own to provide a basic message model.  It uses soft deletion, so that messages, or models that extend from it, can be soft deleted, at which point a task is set up using the very excellent django_q to schedule a hard delete at a time later configured in the settings.

## install
pip install git+https://github.com/millerthegorilla/django_messages.git#egg=django_messages
add django_messages to your installed apps.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'django_messages',
]
```
## settings
You will need to set the site domain in the admin app, and also the settings.BASE_HTML for the statement `{% extends BASE_HTML %}` in the templates where BASE_HTML comes from the context_processor.

You can make the app abstract if you are subclassing it in another app.
```
ABSTRACTMESSAGE = True
```
You can set the timeout before messages (or subclasses of msg - even when message is abstract) are hard deleted.  This effectively means that there will be a copy of a message, for some period of time before it is erased permanently.
```
DELETION_TIMEOUT = { 'POST'(ie model name as string): 'timezone.timedelta(days=21)' }
```
## dependencies
django-crispy-forms==1.11.2
crispy-bootstrap==5 0.6
bleach==3.3.0