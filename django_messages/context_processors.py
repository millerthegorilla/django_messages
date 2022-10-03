from django.conf import settings  # import the settings file
import typing


def base_html(request):
    return {"BASE_HTML": settings.BASE_HTML}


def site_name(request) -> typing.Dict[str, str]:
    return {"siteName": settings.SITE_NAME}
