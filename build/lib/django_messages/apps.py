import os
from collections import OrderedDict

import django
from django.apps import apps
from django.conf import settings

from crispy_forms import templates as crispy_templates
from crispy_bootstrap5 import templates as bs5_templates

APPS = [
    {"name": "django_q", "templates": ""},
    {"name": "crispy_forms", "templates": crispy_templates},
    {"name": "crispy_bootstrap5", "templates": bs5_templates},
]


class DjangoMessagesConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_messages"

    def ready(self) -> None:
        for app in APPS:
            if app["name"] not in settings.INSTALLED_APPS:
                settings.INSTALLED_APPS += (app["name"],)
                apps.app_configs = OrderedDict()
                apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
                apps.clear_cache()
                apps.populate(settings.INSTALLED_APPS)
                if app["templates"] != "":
                    settings.TEMPLATES[0]["DIRS"].append(
                        os.path.abspath(app["templates"].__path__._path[0])
                    )
