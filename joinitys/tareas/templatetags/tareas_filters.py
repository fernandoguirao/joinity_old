from django import template
from joinitys.tareas.models import Usuarios_Tarea, Tareas
from django.shortcuts import get_object_or_404
from notificaciones.models import Notificaciones
register = template.Library()

@register.filter(name='completada')
def completada(value, arg):
    usuario_tarea=get_object_or_404(Usuarios_Tarea, tarea=value, usuario=arg)
    return usuario_tarea.completada

@register.filter(name='ultima')
def ultima(value, arg):
    tarea=Tareas.objects.filter(joinity=value, usuarios__usuario=arg)[0]
    return tarea.nombre

@register.filter(name='visto_tarea')
def visto_tarea(value, arg):
    tareas=Tareas.objects.filter(joinity=value)
    existe=False
    for tarea in tareas:
        if Usuarios_Tarea.objects.filter(usuario=arg, tarea=tarea).exists():
            if Notificaciones.objects.filter(usuario=arg, tipo=3, id_notificacion=tarea.id, estado=1).exists():
                existe=True
    return existe