from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from mensajes.forms import Mandar_Mensaje_Form
from django.shortcuts import  get_object_or_404
from django.contrib.auth.models import User
from mensajes.models import Mensajes
from django.template.loader import render_to_string

@dajaxice_register
def enviar_mensaje(request, formulario, conversador_id):
    conversador=get_object_or_404(User, pk=conversador_id)
    form = Mandar_Mensaje_Form(formulario, user=request.user, destinatario=conversador)
    if form.is_valid():
        form.save()
        return simplejson.dumps({'error':False, 'conversador_id':conversador_id})
    return simplejson.dumps({'error':'Error al enviar'})

@dajaxice_register
def refrescar(request, conversador_id):
    conversador=get_object_or_404(User, pk=conversador_id)
    lista_mensajes=Mensajes.objects.raw("SELECT * FROM Mensajes WHERE (destinatario_id="+str(request.user.id)+" AND remitente_id="+str(conversador.id)+") OR (remitente_id="+str(request.user.id)+" AND destinatario_id="+str(conversador.id)+") ORDER BY id DESC;")
    mensajes=render_to_string('mensajes/ajax_mensajes.html', {"mensajes":lista_mensajes,})
    return simplejson.dumps({'mensajes':mensajes})
