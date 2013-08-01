from django import template
from joinitys.tareas.models import Usuarios_Tarea
from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter(name='completada')
def completada(value, arg):
    usuario_tarea=get_object_or_404(Usuarios_Tarea, tarea=value, usuario=arg)
    return usuario_tarea.completada
