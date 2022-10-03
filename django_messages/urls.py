from django.urls import path
from . import views as messages_views

app_name = "django_messages"

urlpatterns = [
    path("messages/", messages_views.MessageList.as_view(), name="message_list"),
    path(
        "create_message/", messages_views.MessageCreate.as_view(), name="message_create"
    ),
    path(
        "update_message/<int:pk>/<slug:slug>/",
        messages_views.MessageUpdate.as_view(),
        name="message_update",
    ),
    path(
        "delete_message/<int:pk>/<slug:slug>/",
        messages_views.MessageDelete.as_view(),
        name="message_delete",
    ),
    path(
        "<int:pk>/<slug:slug>/",
        messages_views.MessageView.as_view(),
        name="message_view",
    ),
]
