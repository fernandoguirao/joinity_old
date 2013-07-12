from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from joinitys.models import Joinitys
from forms import Crear_Evento, Anyadir_Lugar
from models import Eventos, Usuarios_Evento, Lugares_Evento

@login_required
def crear_evento(request, joinity_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    if request.POST:
        formulario=Crear_Evento(request.POST, request.FILES, user=request.user, joinity=joinity)
        if formulario.is_valid:
            evento=formulario.save()
            evento=get_object_or_404(Eventos, pk=evento.id)
            u=Usuarios_Evento(usuario_id=request.user.id, evento=evento, estado=2)
            u.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/evento/crear/2/"+str(evento.id))

    else:
        formulario=Crear_Evento(instance=request.user, user=request.user, joinity=joinity)
    context={"formulario":formulario, "joinity":joinity, "usuario":request.user}
    return render_to_response("eventos/crear_evento.html", context, context_instance=RequestContext(request))
@login_required
def crear_evento_2(request, joinity_id, evento_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    state="Anyadir Lugares"
    if request.POST:
        formulario=Anyadir_Lugar(request.POST)
        state="Anyadido Lugar"
        if formulario.is_valid:
            n=evento.lugares_evento.count()
            n+=1
            nuevo=Lugares_Evento(evento=evento, lugar=request.POST["lugar"], n=n)
            nuevo.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/evento/crear/2/"+str(evento.id))
    else:
        formulario=Anyadir_Lugar()
    context={"joinity": joinity, "evento": evento,"formulario":formulario, "state": state, "pagina":"anyadir_lugares", "usuario":request.user}
    return render_to_response('eventos/crear_evento.html', context, context_instance=RequestContext(request))

@login_required
def crear_evento_3(request, joinity_id, evento_id):
    state = "Invitar usuarios"
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    usuarios_invitados=[]
    usuarios_evento=Usuarios_Evento.objects.filter(evento=evento)
    for user in usuarios_evento:
        usuarios_invitados.append(user.usuario)

    context={"state":state, "joinity": joinity, "evento": evento, "usuarios_invitados": usuarios_invitados, "usuario":request.user, "pagina":"invitar"}
    return render_to_response('eventos/crear_evento.html', context, context_instance=RequestContext(request))
