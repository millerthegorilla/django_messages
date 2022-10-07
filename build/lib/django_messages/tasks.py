import logging

from . import models as messages_models

logger = logging.getLogger("django_artisan")


def schedule_hard_delete(
    slug=None, deleted_at=None, type=None, id=None, **kwargs
) -> None:

    try:
        messages_models.Message.all_objects.get(id=int(id)).hard_delete()
        return "Succesfully hard deleted message!"
    except messages_models.Message.DoesNotExist:
        return "Failure - unable to find that message to hard delete..."
