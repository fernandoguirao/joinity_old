from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from joinitys.models import Joinitys, Usuarios_Joinity
from models import Usuarios_Tarea, Tareas, Lugares_Tarea
from forms import Crear, Anyadir_Lugar

@login_required
def mis_tareas(request):
    lista_tareas=Usuarios_Tarea.objects.filter(usuario=request.user)
    context={'lista_tareas':lista_tareas, "pagina":"misTareas"}
    return render(request, 'mistareas/mistareas.html', context)
@login_required
def ver(request, joinity_id, tarea_id):
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    lista_admins=Usuarios_Tarea.objects.filter(tarea=tarea, estado=2)
    context={"tarea": tarea, "lista_admins": lista_admins}
    return render_to_response("ver_tarea.html", context)
@login_required
def crear(request, joinity_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    if request.POST:
        formulario=Crear(request.POST, request.FILES, user=request.user, joinity=joinity)
        if formulario.is_valid:
            tarea=formulario.save()
            tarea=get_object_or_404(Tareas, pk=tarea.id)
            u=Usuarios_Tarea(usuario_id=request.user.id, tarea=tarea, estado=2)
            u.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))

    else:
        formulario=Crear(instance=request.user, user=request.user, joinity=joinity)
    context={"formulario":formulario, "joinity":joinity}
    return render_to_response("crear_tarea.html", context, context_instance=RequestContext(request))
@login_required
def crear_subtarea(request, joinity_id, tarea_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    padre=get_object_or_404(Tareas, pk=tarea_id)
    if request.POST:
        formulario=Crear(request.POST, request.FILES, user=request.user, joinity=joinity)
        if formulario.is_valid:
            tarea=formulario.save()
            tarea=get_object_or_404(Tareas, pk=tarea.id)
            tarea.padre=padre
            tarea.save()
            u=Usuarios_Tarea(usuario_id=request.user.id, tarea=tarea, estado=2)
            u.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))

    else:
        formulario=Crear(instance=request.user, user=request.user, joinity=joinity)
    context={"formulario":formulario, "joinity":joinity}
    return render_to_response("crear_tarea.html", context, context_instance=RequestContext(request))
@login_required
def crear_2(request, joinity_id, tarea_id):
    state = "Invitar usuarios"
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuarios_invitados=[]
    usuarios_tarea=Usuarios_Tarea.objects.filter(tarea=tarea)
    for user in usuarios_tarea:
        usuarios_invitados.append(user.usuario)

    context={"state":state, "joinity": joinity, "tarea": tarea, "usuarios_invitados": usuarios_invitados}
    return render_to_response('crear_tarea_2.html', context, context_instance=RequestContext(request))

@login_required
def crear_3(request, joinity_id, tarea_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    state="Anyadir Lugares"
    if request.POST:
        formulario=Anyadir_Lugar(request.POST)
        state="Anyadido Lugar"
        if formulario.is_valid:
            n=tarea.lugares_tarea.count()
            n+=1
            nuevo=Lugares_Tarea(tarea=tarea, lugar=request.POST["lugar"], n=n)
            nuevo.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/3/"+str(tarea.id))
    else:
        formulario=Anyadir_Lugar()
    context={"joinity": joinity, "tarea": tarea,"formulario":formulario, "state": state}
    return render_to_response('crear_tarea_3.html', context, context_instance=RequestContext(request))
@login_required
def invitar(request, joinity_id, tarea_id, usuario_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuario=get_object_or_404(User, pk=usuario_id)
    if Usuarios_Tarea.objects.filter(usuario=usuario, tarea=tarea).count()==0:
        nuevo=Usuarios_Tarea(usuario=usuario, tarea=tarea, estado=0)
        nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))
@login_required
def invitar_todos(request, joinity_id, tarea_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuarios_joinity=Usuarios_Joinity.objects.filter(joinity=joinity)
    for usuario in usuarios_joinity:
        print usuario.usuario.first_name
        if Usuarios_Tarea.objects.filter(usuario=usuario.usuario, tarea=tarea).count()==0:
            nuevo=Usuarios_Tarea(usuario=usuario.usuario, tarea=tarea, estado=0)
            nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))

