from crispy_forms import layout, helper

from django import forms, utils, conf

import bleach
import html

from . import models as messages_models


class Message(forms.ModelForm):
    class Meta:
        model = messages_models.Message
        fields = [
            "text",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "",
                layout.Field("text", css_class="mb-3 message-create-form-text"),
                layout.Submit("save", "Save Message", css_class="col-3 mt-3"),
            )
        )
        self.helper.form_id = "id-message-create-form"
        self.helper.form_method = "post"
        self.helper.form_class = "col-auto"
        self.helper.form_action = "django_messages:message_create"

    def clean_text(self) -> str:
        return self.sanitize_text(self.cleaned_data["text"])

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
