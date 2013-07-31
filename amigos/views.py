# Create your views here
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from amigos.forms import Invitar_Amigo
from django.http import HttpResponseRedirect
from amigos.models import Amigos
from django.shortcuts import  get_object_or_404
from django.contrib.auth.models import User

@login_required
def invitar(request):
    if request.POST:
        formulario = Invitar_Amigo(request.POST, user=request.user)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = Invitar_Amigo(instance=request.user.usuario, user=request.user)
    context = {'formulario':formulario}
    return render_to_response('invitar.html', context, context_instance=RequestContext(request))  # Create your views here.
def invitar_usuario(request, amigo_id):
    amigo = get_object_or_404(User, pk=amigo_id)
    if not (Amigos.objects.filter(usuario=request.user, amigo=amigo).exists() or Amigos.objects.filter(usuario=amigo, amigo=request.user).exists()):
        nuevo_amigo = Amigos(usuario=request.user, amigo=amigo, estado=1)
        nuevo_amigo.save()
    return HttpResponseRedirect('/usuario/' + amigo_id)

def lista_amigos(request):
    solicitudes = Amigos.objects.filter(amigo=request.user, estado=0)
    lista_amigos = Amigos.objects.filter(usuario=request.user, estado=1)
    context = {"amigos": lista_amigos, "solicitudes":solicitudes}
    return render_to_response('lista_amigos.html', context)
def aceptar(request, amigo_id):
    solicitud = get_object_or_404(Amigos, pk=amigo_id)
    nuevo_amigo = Amigos(usuario=request.user, amigo=solicitud.usuario, estado=1)
    solicitud.estado = 1
    solicitud.save()
    nuevo_amigo.save()
    return HttpResponseRedirect('/amigo/')


    
