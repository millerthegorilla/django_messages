from django import conf, urls, utils
from django.db import models, DEFAULT_DB_ALIAS
from django.contrib import auth
from django.template import defaultfilters


from . import soft_deletion

# django_messages.forms.Message.sanitize_text is a static function that uses bleach
# to sanitize text.  It is called in form.clean_text() but if you create a model,
# and want to sanitize the text, you can do it manually.


class Message(soft_deletion.Model):
    author: models.ForeignKey = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
    )
    text: models.TextField = models.TextField(max_length=500)
    moderation_date: models.DateField = models.DateField(
        null=True, default=None, blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    slug: models.SlugField = models.SlugField(unique=True, db_index=True, max_length=80)

    def get_author_name(self) -> str:
        author = self.author
        if author is None:
            return "anonymous"
        else:
            return author.username

    def __str__(self) -> str:
        return f"'{self.text}' by {self.get_author_name()}"

    def __repr__(self) -> str:
        return f"{self.text}"

    def get_absolute_url(self) -> str:
        return urls.reverse_lazy(
            "django_messages:message_view", args=[self.id, self.slug]
        )  # type: ignore

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=DEFAULT_DB_ALIAS,
        update_fields=None,
    ):
        self.slug = defaultfilters.slugify(
            self.text[:10]
            + "-"
            + str(utils.dateformat.format(utils.timezone.now(), "Y-m-d H:i:s"))
        )
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ["-created_at"]
        app_label = "django_messages"

        try:
            abstract = conf.settings.ABSTRACTMESSAGE
        except AttributeError:
            abstract = False


# class Moderation(models.Model):
# TODO make moderation mixin
#     author: models.ForeignKey = models.ForeignKey(
#         auth.get_user_model(), on_delete=models.SET_NULL, null=True, related_name="moderations")
#     moderation_date: models.DateField = models.DateField(null=True, default=None, blank=True)

#     class Meta:
#         abstract = True
