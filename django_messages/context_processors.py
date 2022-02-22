from django.conf import settings # import the settings file

def base_html(request):
    return {'BASE_HTML': settings.BASE_HTML}