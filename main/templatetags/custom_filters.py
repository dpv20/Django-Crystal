from django import template

register = template.Library()

@register.filter
def to(value, end_value):
    return range(value, end_value + 1)

from django import template
import datetime

register = template.Library()

@register.filter
def add(value, days):
    try:
        return value + datetime.timedelta(days=days)
    except:
        return value
