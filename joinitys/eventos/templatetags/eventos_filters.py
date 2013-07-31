from django import template
register = template.Library()
from notificaciones.models import Notificaciones
@register.filter(name='visto')
def visto(value, arg):
    return Notificaciones.objects.filter(usuario=arg, tipo=2, id_notificacion=value.id).exists()
