from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from mensajes.forms import Mandar_Mensaje_Form
from django.http import HttpResponseRedirect
from mensajes.models import Mensajes
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404

@login_required
def escribir(request):
    if request.POST:
        formulario = Mandar_Mensaje_Form(request.POST, user=request.user)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = Mandar_Mensaje_Form(instance=request.user.usuario, user=request.user)
    context = {'formulario':formulario}
    return render_to_response('escribir_mensaje.html', context, context_instance=RequestContext(request))  # Create your views here.
@login_required
def inbox(request):
    subconsulta1="SELECT remitente_id FROM Mensajes WHERE destinatario_id="+str(request.user.id)
    subconsulta2="SELECT destinatario_id FROM Mensajes WHERE remitente_id="+str(request.user.id)
    consulta="SELECT * FROM auth_user WHERE id IN ("+subconsulta1+") OR id IN ("+subconsulta2+");"
    usuarios=User.objects.raw(consulta)
    conversador=get_object_or_404(User, pk=usuarios[0].id)
    lista_mensajes=Mensajes.objects.raw("SELECT * FROM Mensajes WHERE (destinatario_id="+str(request.user.id)+" AND remitente_id="+str(conversador.id)+") OR (remitente_id="+str(request.user.id)+" AND destinatario_id="+str(conversador.id)+") ORDER BY id DESC;")

    #if request.POST:
    #    formulario = Mandar_Mensaje_Form(request.POST, user=request.user, destinatario=conversador)
    #    if formulario.is_valid:
    #        formulario.save()
    #else:
    formulario = Mandar_Mensaje_Form(instance=request.user.usuario, user=request.user, destinatario=conversador)
    context = {"mensajes": lista_mensajes, "pagina":"misMensajes", "usuarios":usuarios, "formulario":formulario, "usuario":request.user, "conversador":conversador}
    return render_to_response('mensajes/inbox.html', context, context_instance=RequestContext(request))
def chat(request, user_id):
    conversador=get_object_or_404(User, pk=user_id)
    lista_mensajes=Mensajes.objects.raw("SELECT * FROM Mensajes WHERE (destinatario_id="+str(request.user.id)+" AND remitente_id="+str(user_id)+") OR (remitente_id="+str(request.user.id)+" AND destinatario_id="+str(user_id)+") ORDER BY id DESC;")
    subconsulta1="SELECT remitente_id FROM Mensajes WHERE destinatario_id="+str(request.user.id)
    subconsulta2="SELECT destinatario_id FROM Mensajes WHERE remitente_id="+str(request.user.id)
    consulta="SELECT * FROM auth_user WHERE id IN ("+subconsulta1+") OR id IN ("+subconsulta2+");"
    usuarios=User.objects.raw(consulta)
    if request.POST:
        formulario = Mandar_Mensaje_Form(request.POST, user=request.user, destinatario=conversador)
        if formulario.is_valid:
            formulario.save()
    else:
        formulario = Mandar_Mensaje_Form(instance=request.user.usuario, user=request.user, destinatario=conversador)
    context = {"mensajes": lista_mensajes, "pagina":"misMensajes", "usuarios":usuarios, "formulario":formulario, "usuario":request.user}
    return render_to_response('mensajes/inbox.html', context, context_instance=RequestContext(request))
def ver(request, mensaje_id):
    mensaje = get_object_or_404(Mensajes, pk=mensaje_id)
    if(mensaje.destinatario != request.user):
        mensaje = False
    else:
        mensaje.estado = 1
        mensaje.save()
    context = {"mensaje": mensaje}
    return render_to_response('ver.html', context)
# Create your views here.
