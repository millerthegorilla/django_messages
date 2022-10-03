from django.contrib import admin
from django.urls import path, include
from django_messages import urls as messages_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(messages_urls)),
    # path("__debug__/", include("debug_toolbar.urls")),
]
