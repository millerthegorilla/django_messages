import uuid
import logging

from django.db import models
from django.contrib import admin
from django import utils, conf, http
from django.utils import timezone

from django_q import tasks

# The below is from https://adriennedomingus.com/blog/soft-deletion-in-django
# with djangoq added... :)

logger = logging.getLogger("django_artisan")


class QuerySet(models.query.QuerySet):
    def delete(self) -> int:
        for q in self.all():
            q.delete()
        return super(QuerySet, self)

    def hard_delete(self) -> tuple[int, dict]:
        return super(QuerySet, self).delete()

    def alive(self) -> models.query.QuerySet:
        return self.filter(deleted_at=None)

    def dead(self) -> models.query.QuerySet:
        return self.exclude(active=False)


class Manager(models.Manager):
    def __init__(self, *args, **kwargs) -> None:
        self.alive_only = kwargs.pop("alive_only", True)
        super(Manager, self).__init__(*args, **kwargs)

    def get_queryset(self) -> models.query.QuerySet:
        if self.alive_only:
            return QuerySet(self.model).filter(active=True)
        return QuerySet(self.model)

    def hard_delete(self) -> None:
        self.get_queryset().hard_delete()


class Model(models.Model):
    active: models.BooleanField = models.BooleanField(default="True")
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = Manager()
    all_objects = Manager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, deletion_timeout: timezone.timedelta = None) -> None:
        if self.active:
            self.deleted_at = utils.timezone.now()
            self.active = False
            self.save(update_fields=["deleted_at", "active"])
            # can override by defining deletion_timeout
            timeout = conf.settings.DELETION_TIMEOUT.get(
                str(self),
                deletion_timeout if deletion_timeout else timezone.timedelta(days=21),
            )
            try:
                tasks.schedule(
                    "django_messages.tasks.schedule_hard_delete",
                    name="sd_timeout_" + str(uuid.uuid4()),
                    schedule_type="O",
                    repeats=-1,
                    next_run=utils.timezone.now() + timeout,
                    id=str(self.id),
                    app_label=self._meta.app_label,
                    model_name=self._meta.model_name,
                )
            except Exception as e:
                logger.error("unable to schedule task : {0}".format(str(e)))

    def hard_delete(self) -> None:
        """
        called by posts_and_comments.tasks.schedule_hard_delete
        """
        super(Model, self).delete()


class Admin(admin.ModelAdmin):
    def get_queryset(self, request: http.HttpRequest) -> models.query.QuerySet:
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to
        # prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request: http.HttpRequest, qs: QuerySet) -> None:
        qs.hard_delete()
