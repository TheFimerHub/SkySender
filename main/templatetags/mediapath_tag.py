from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name='mediapath')
def mediapath(value):
    media_url = settings.MEDIA_URL
    return f"{media_url}{value}"
