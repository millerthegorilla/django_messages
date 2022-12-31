import logging

from django.apps import apps

logger = logging.getLogger("django_artisan")


def schedule_hard_delete(id, app_label, model_name, **kwargs) -> None:

    try:
        model = apps.get_model(app_label, model_name)
        messages_models.Message.all_objects.get(id=int(id)).hard_delete()
        return "Succesfully hard deleted message!"
    except messages_models.Message.DoesNotExist:
        return "Failure - unable to find that message to hard delete..."
