import logging

from django import urls, utils
from django.contrib.auth import get_user_model
from django.views import generic

from django.views.decorators import cache

from . import models as messages_models
from . import forms as messages_forms

User = get_user_model()

logger = logging.getLogger("django_artisan")


@utils.decorators.method_decorator(cache.never_cache, name="dispatch")
class MessageList(generic.list.ListView):
    model = messages_models.Message
    template_name = "django_messages/message_list.html"
    paginate_by = 6


@utils.decorators.method_decorator(cache.never_cache, name="dispatch")
@utils.decorators.method_decorator(cache.never_cache, name="get")
class MessageView(generic.DetailView):
    model = messages_models.Message
    slug_url_kwarg = "slug"
    slug_field = "slug"
    template_name = "django_messages/message_detail.html"
    form_class = messages_forms.Message
    context_object_name = "message"


class MessageUpdate(generic.UpdateView):
    model = messages_models.Message
    form_class = messages_forms.Message
    template_name_suffix = "_create"
    extra_context = {"instructions": "Update your message..."}

    def form_valid(self, form):
        return super().form_valid()
        pass

    def form_invalid(self, form):
        return super().form_invalid(form)
        pass


class MessageDelete(generic.edit.DeleteView):
    model = messages_models.Message
    template_name = "django_messages/message_delete.html"
    success_url = urls.reverse_lazy("django_messages:message_list")


class MessageCreate(generic.edit.CreateView):
    model = messages_models.Message
    template_name_suffix = "_create"
    form_class = messages_forms.Message
    extra_context = {"instructions": "Create your message..."}
