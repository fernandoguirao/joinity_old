from dajaxice.decorators import dajaxice_register
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext
from forms import FormComentario
from models import Actualizaciones_Eventos

from models import Eventos
from forms import FormTexto
@dajaxice_register
def postear(request, formulario, evento_id):
    evento=get_object_or_404(Eventos, pk=evento_id)
    form = FormTexto(formulario, usuario=request.user, evento=evento)
    if form.is_valid():
        form.save()
        return simplejson.dumps({'status':False, 'evento_id':evento_id})
    return simplejson.dumps({'status': 'Error al enviar'})

@dajaxice_register
def refrescar(request, evento_id):
    evento=get_object_or_404(Eventos, pk=evento_id)
    comentar=FormComentario(usuario=request.user, actualizacion=0)
    muro=render_to_string('eventos/ajax_muro.html', {"evento":evento, "comentar":comentar,},context_instance=RequestContext(request))
    return simplejson.dumps({'muro':muro})

@dajaxice_register
def comentar(request, formulario, actualizacion_id):
    actualizacion=get_object_or_404(Actualizaciones_Eventos, pk=actualizacion_id)
    form = FormComentario(formulario, usuario=request.user, actualizacion=actualizacion)
    if form.is_valid():
        form.save()
        return simplejson.dumps({'status':False, 'evento_id':actualizacion.evento.id})
    return simplejson.dumps({'status': 'Error al enviar'})