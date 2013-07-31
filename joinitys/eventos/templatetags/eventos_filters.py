from django import template
register = template.Library()
from joinitys.eventos.models import Usuarios_Evento

@register.filter(name='visto')
def visto(value, arg):
    usuario_evento=Usuarios_Evento.objects.get(usuario=arg, evento=value)
    return usuario_evento.estado==1
