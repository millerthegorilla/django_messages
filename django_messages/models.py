import bleach
import html
from django import conf, urls, utils
from django.db import models, DEFAULT_DB_ALIAS
from django.contrib import auth
from django.template import defaultfilters


from . import soft_deletion

# Create your models here.


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

    def get_absolute_url(self, a_name="django_messages") -> str:
        return urls.reverse_lazy(
            a_name + ":message_view", args=[self.id, self.slug]
        )  # type: ignore

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=DEFAULT_DB_ALIAS,
        update_fields=None,
    ):
        self.sanitize_text(self.text)
        self.slug = defaultfilters.slugify(
            self.text[:10]
            + "-"
            + str(utils.dateformat.format(utils.timezone.now(), "Y-m-d H:i:s"))
        )
        super().save(force_insert, force_update, using, update_fields)

    @staticmethod
    def sanitize_text(text: str) -> utils.safestring.SafeString:
        return utils.safestring.mark_safe(
            bleach.clean(
                html.unescape(text),
                tags=conf.settings.ALLOWED_TAGS,
                attributes=conf.settings.ATTRIBUTES,
                css_sanitizer=conf.settings.CSS_SANITIZER,
                strip=True,
                strip_comments=True,
            )
        )

    class Meta:
        ordering = ["-created_at"]
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
