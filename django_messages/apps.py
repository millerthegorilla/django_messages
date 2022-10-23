import os
import importlib
from collections import OrderedDict

from django.apps import apps, AppConfig
from django.conf import settings
from django.core.management import call_command

from crispy_forms import templates as crispy_templates
from crispy_bootstrap5 import templates as bs5_templates

my_apps = [
    {"name": "django_q", "templates": ""},
    {"name": "crispy_forms", "templates": crispy_templates},
    {"name": "crispy_bootstrap5", "templates": bs5_templates},
]


class DjangoMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_messages"

    def ready(self) -> None:
        global my_apps
        sdir = False
        for app in my_apps:
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
                static = os.path.abspath(
                    importlib.import_module(app["name"]).__path__[0] + "/static/"
                )
                if os.path.isdir(static):
                    sdir = True
                    settings.STATICFILES_DIRS += [static]
                try:
                    theapp = importlib.import_module(app["name"] + ".apps")
                    my_apps += theapp.my_apps
                    theapp.setup_apps()
                except (ModuleNotFoundError, AttributeError):
                    pass
        if sdir:
            call_command("collectstatic", verbosity=0, interactive=False)
