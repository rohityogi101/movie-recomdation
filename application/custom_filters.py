# range function won't work so use zip
from django import template

register = template.Library()

@register.filter
def zip_lists(movies_name, movies_poster):
    return zip(movies_name, movies_poster)
