from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.shortcuts import get_object_or_404
from joinitys.tareas.models import Tareas, Usuarios_Tarea

@dajaxice_register
def marcar_tarea(request, tarea_id):
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuario_tarea=Usuarios_Tarea.objects.get_or_create(usuario=request.user, tarea=tarea)[0]
    if usuario_tarea.completada:
        usuario_tarea.completada=False
    else:
        usuario_tarea.completada=True
    usuario_tarea.save()
    return simplejson.dumps({'completada':usuario_tarea.completada})