from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from joinitys.models import Joinitys, Usuarios_Joinity
from forms import Crear_Evento, Anyadir_Lugar
from models import Eventos, Usuarios_Evento, Lugares_Evento
from django.contrib.auth.models import User
from notificaciones.models import Notificaciones
 
def ver(request, joinity_id, evento_id):
    evento=get_object_or_404(Eventos, pk=evento_id)
    lista_admins=Usuarios_Evento.objects.filter(evento=evento, estado=2)
    context={"evento": evento, "lista_admins": lista_admins}
    return render_to_response("ver_evento.html", context)

@login_required
def crear(request, joinity_id):
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
def crear_2(request, joinity_id, evento_id):
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
def crear_3(request, joinity_id, evento_id):
    state = "Invitar usuarios"
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    usuarios_invitados=[]
    usuarios_evento=Usuarios_Evento.objects.filter(evento=evento)
    for user in usuarios_evento:
        usuarios_invitados.append(user.usuario)

    context={"state":state, "joinity": joinity, "evento": evento, "usuarios_invitados": usuarios_invitados, "usuario":request.user, "pagina":"invitar"}
    return render_to_response('eventos/crear_evento.html', context, context_instance=RequestContext(request))

def invitar(request, joinity_id, evento_id, usuario_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    usuario=get_object_or_404(User, pk=usuario_id)
    if Usuarios_Evento.objects.filter(usuario=usuario, evento=evento).count()==0:
        nuevo=Usuarios_Evento(usuario=usuario, evento=evento, estado=0)
        nuevo.save()
        notificacion=Notificaciones(usuario=usuario, tipo=2, id_notificacion=evento.id)
        notificacion.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/evento/crear/3/"+str(evento.id))
def invitar_todos(request, joinity_id, evento_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    usuarios_joinity=Usuarios_Joinity.objects.filter(joinity=joinity)
    for usuario in usuarios_joinity:
        print usuario.usuario.first_name
        if Usuarios_Evento.objects.filter(usuario=usuario.usuario, evento=evento).count()==0:
            nuevo=Usuarios_Evento(usuario=usuario.usuario, evento=evento, estado=0)
            nuevo.save()
            notificacion=Notificaciones(usuario=usuario, tipo=2, id_notificacion=evento.id)
            notificacion.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/evento/crear/3/"+str(evento.id))
def mis_eventos(request):
    subconsulta="SELECT evento_id FROM Usuarios_Eventos WHERE usuario_id ="+str(request.user.id)
    consulta="SELECT * FROM Eventos WHERE id IN ("+subconsulta+")"
    eventos=Eventos.objects.raw(consulta)
    context={'eventos':eventos, "pagina":"misEventos", "usuario":request.user}
    return render(request, 'eventos/index.html', context)

def ver_mi_evento(request, evento_id):
    subconsulta="SELECT evento_id FROM Usuarios_Eventos WHERE usuario_id ="+str(request.user.id)
    consulta="SELECT * FROM Eventos WHERE id IN ("+subconsulta+")"
    eventos=Eventos.objects.raw(consulta)
    single=get_object_or_404(Eventos, pk=evento_id)
    context={'eventos':eventos, "pagina":"misEventos", "single":single, "usuario":request.user}
    return render(request, 'eventos/index.html', context)
