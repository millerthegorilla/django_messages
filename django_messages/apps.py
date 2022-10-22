import os
import importlib
from collections import OrderedDict

from django.apps import apps, AppConfig
from django.conf import settings

from crispy_forms import templates as crispy_templates
from crispy_bootstrap5 import templates as bs5_templates

my_apps = [
    {"name": "django_q", "templates": ""},
    {"name": "crispy_forms", "templates": crispy_templates},
    {"name": "crispy_forms_tags", "templates": ""},
    {"name": "crispy_bootstrap5", "templates": bs5_templates},
]


class DjangoMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_messages"

    def ready(self) -> None:
        global my_apps
        for app in my_apps:
            if app["name"] not in settings.INSTALLED_APPS:
                theapp = importlib.import_module(app["name"] + ".apps")
                try:
                    my_apps += theapp.my_apps
                except AttributeError:
                    pass
                settings.INSTALLED_APPS += (app["name"],)
                apps.app_configs = OrderedDict()
                apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
                apps.clear_cache()
                apps.populate(settings.INSTALLED_APPS)
                if app["templates"] != "":
                    settings.TEMPLATES[0]["DIRS"].append(
                        os.path.abspath(app["templates"].__path__._path[0])
                    )
