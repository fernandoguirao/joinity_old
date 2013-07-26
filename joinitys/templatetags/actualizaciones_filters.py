from django import template
from datetime import date
register = template.Library()

@register.filter(name='es_hoy')
def es_hoy(value):
    delta = value.date() - date.today()
    if delta.days == 0:
        return True
    else:
        return False