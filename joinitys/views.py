from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import FormTexto, Crear_Evento, Crear_Tarea
from forms import FormFoto, Anyadir_Lugar_Evento, Anyadir_Lugar_Tarea
from forms import Buscar as Buscar_Reserva, Reservar, FormComentario
from django.contrib.auth.decorators import login_required
from models import Usuarios_Joinity, Eventos, Tareas, Usuarios_Tarea, Usuarios_Evento, Actualizaciones
from models import Lugares_Evento, Lugares_Tarea, Reservas_Empresas, Joinitys, Joinitys_VIP, Compras, Aficiones
from django.http import HttpResponseRedirect
from django.shortcuts import  render, get_object_or_404
from django.contrib.auth.models import User
from joinity.settings import LOCALHOST
from django.core.mail import send_mail
from reservas.models import Empresa
from categorias.models import Subcategorias_Compras, Categorias_Compras, Subcategorias, Categorias
def index(request):
    if not request.user.is_authenticated():
        usuario=False
    else:
        usuario=request.user
        if not request.user.first_name:
            return HttpResponseRedirect('/usuario/editar/')
    # lista_pagos = Pagos.objects.filter(usuarios=request.user.id).order_by('id')
    #lista_joinitys = Usuarios_Joinity.objects.filter(usuario=request.user)
    lista_aficiones=Joinitys.objects.filter(tipo="3")
    lista_compras=Joinitys.objects.filter(tipo="2")
    lista_family=Joinitys.objects.filter(tipo="1")
    lista_vip=Joinitys_VIP.objects.all()
    context = {'lista_aficiones': lista_aficiones, 'lista_compras':lista_compras, 'lista_family':lista_family, "usuario":usuario, "pagina":"home", "cinco":[1,2,3,4,5], "VIP":lista_vip}
    return render(request, 'index/index.html', context)



@login_required
def mis_joinitys(request):
    lista_joinitys=Usuarios_Joinity.objects.filter(usuario=request.user)
    context={'lista_joinitys':lista_joinitys, "usuario":request.user, "pagina":"joinity"}
    return render(request, 'misjoinitys/misjoinitys.html', context)
@login_required
def filtro(request):
    if request.GET:
        tipo=request.GET.get("herolist", -1)
        if tipo=="0":
            categoria=get_object_or_404(Categorias_Compras, pk=request.GET.get("comprar2", 0))
            subcategorias=Subcategorias_Compras.objects.filter(categoria=categoria)
            compras=Compras.objects.filter(subcategoria__in=subcategorias)
            rangoprecios=request.GET.get("comprar3", -1)
            if rangoprecios=="0":
                precio_min=0
                precio_max=200
            elif rangoprecios=="1":
                precio_min=200
                precio_max=400
            elif rangoprecios=="2":
                precio_min=400
                precio_max=1000
            elif rangoprecios=="3":
                precio_min=1000
                precio_max=-1
            lista_joinitys=[]
            for compra in compras:
                if compra.joinity.precio>=precio_min and (precio_max==-1 or compra.joinity.precio<=precio_max):
                    lista_joinitys.append(compra)
        elif tipo=="1":
            categoria=get_object_or_404(Categorias, pk=request.GET.get("aficion2", 0))
            subcategorias=Subcategorias.objects.filter(categoria=categoria)
            ciudad=request.GET.get("aficion3", "")
            aficiones=Aficiones.objects.filter(subcategoria__in=subcategorias)
            if ciudad!="":
                lista_joinitys=[]
                for aficion in aficiones:
                    for lugar in aficion.joinity.lugares.all():
                        if lugar.lugar==ciudad and aficion not in lista_joinitys:
                            lista_joinitys.append(aficion)
            else:
                lista_joinitys=aficiones

        else:
            lista_joinitys=Usuarios_Joinity.objects.filter(usuario=request.user)

    context={'lista_joinitys':lista_joinitys, "usuario":request.user, "pagina":"joinity"}
    return render(request, 'misjoinitys/misjoinitys.html', context)



@login_required
def mis_tareas(request):
    lista_tareas=Usuarios_Tarea.objects.filter(usuario=request.user)
    context={'lista_tareas':lista_tareas, "pagina":"misTareas"}
    return render(request, 'mistareas/mistareas.html', context)
@login_required
def ver(request, joinity_id):
    # What you want the button to do.
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    if request.user.is_authenticated():
        soy=joinity.que_soy(request.user)
    else:
        soy="desconectado"
    if request.POST:
        es_contenido=request.GET.get("contenido", False)
        es_comentario=request.GET.get("comentar", False)
        if es_contenido:
            if es_contenido=="texto":
                form = FormTexto(request.POST, usuario=request.user, joinity=joinity)
            elif es_contenido=="foto":
                form = FormFoto(request.POST, request.FILES, joinity=joinity, usuario=request.user)
            comentar=FormComentario(instance=request.user, usuario=request.user, actualizacion=0)
            if form.is_valid:
                form.save()
                return HttpResponseRedirect("/joinity/ver/"+str(joinity.id))
        elif es_comentario:
            actualizacion=get_object_or_404(Actualizaciones, pk=es_comentario)
            form = FormTexto(instance=request.user, usuario=request.user, joinity=joinity)
            comentar=FormComentario(request.POST, usuario=request.user, actualizacion=actualizacion)
            if comentar.is_valid:
                comentar.save()
                return HttpResponseRedirect("/joinity/ver/"+str(joinity.id))

        else:
            form = FormTexto(instance=request.user, usuario=request.user, joinity=joinity)
            comentar=FormComentario(instance=request.user, usuario=request.user, actualizacion=0)

    else:
        form = FormTexto(instance=request.user, usuario=request.user, joinity=joinity)
        comentar=FormComentario(instance=request.user, usuario=request.user, actualizacion=0)
    context = {"joinity": joinity, "form": form, "cinco":[1,2,3,4,5],
               "pagina":"joinity", "comentar":comentar,
               "usuario":request.user, "soy":soy}
    return render_to_response("single/joinity.html", context, context_instance=RequestContext(request))


def aceptar(request, joinity_id):
    usuario_joinity=get_object_or_404(Usuarios_Joinity, joinity=joinity_id, usuario=request.user)
    if usuario_joinity.estado==0:
        usuario_joinity.estado=1
        usuario_joinity.save()
    return HttpResponseRedirect("/joinity/ver/"+str(usuario_joinity.joinity.id))


def unirse(request, joinity_id):
    if request.user.is_authenticated():
        joinity = get_object_or_404(Joinitys, pk=joinity_id)
        if joinity.privacidad==0:
            nuevo=Usuarios_Joinity(joinity=joinity, usuario=request.user, estado=1)
            nuevo.save()
        elif joinity.privacidad==1:
            nuevo=Usuarios_Joinity(joinity=joinity, usuario=request.user, estado=-1)
            nuevo.save()
        return HttpResponseRedirect("/joinity/ver/"+str(joinity.id))
    return HttpResponseRedirect("/")

    
def ver_evento(request, joinity_id, evento_id):
    evento=get_object_or_404(Eventos, pk=evento_id)
    lista_admins=Usuarios_Evento.objects.filter(evento=evento, estado=2)
    context={"evento": evento, "lista_admins": lista_admins}
    return render_to_response("ver_evento.html", context)


def ver_tarea(request, joinity_id, tarea_id):
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    lista_admins=Usuarios_Tarea.objects.filter(tarea=tarea, estado=2)
    context={"tarea": tarea, "lista_admins": lista_admins}
    return render_to_response("ver_tarea.html", context)

def invitar_evento(request, joinity_id, evento_id, usuario_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    usuario=get_object_or_404(User, pk=usuario_id)
    if Usuarios_Evento.objects.filter(usuario=usuario, evento=evento).count()==0:
        nuevo=Usuarios_Evento(usuario=usuario, evento=evento, estado=0)
        nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/evento/crear/3/"+str(evento.id))
def invitar_todos_evento(request, joinity_id, evento_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    evento=get_object_or_404(Eventos, pk=evento_id)
    usuarios_joinity=Usuarios_Joinity.objects.filter(joinity=joinity)
    for usuario in usuarios_joinity:
        print usuario.usuario.first_name
        if Usuarios_Evento.objects.filter(usuario=usuario.usuario, evento=evento).count()==0:
            nuevo=Usuarios_Evento(usuario=usuario.usuario, evento=evento, estado=0)
            nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/evento/crear/3/"+str(evento.id))

def crear_tarea(request, joinity_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    if request.POST:
        formulario=Crear_Tarea(request.POST, request.FILES, user=request.user, joinity=joinity)
        if formulario.is_valid:
            tarea=formulario.save()
            tarea=get_object_or_404(Tareas, pk=tarea.id)
            u=Usuarios_Tarea(usuario_id=request.user.id, tarea=tarea, estado=2)
            u.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))

    else:
        formulario=Crear_Tarea(instance=request.user, user=request.user, joinity=joinity)
    context={"formulario":formulario, "joinity":joinity}
    return render_to_response("crear_tarea.html", context, context_instance=RequestContext(request))
def crear_subtarea(request, joinity_id, tarea_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    padre=get_object_or_404(Tareas, pk=tarea_id)
    if request.POST:
        formulario=Crear_Tarea(request.POST, request.FILES, user=request.user, joinity=joinity)
        if formulario.is_valid:
            tarea=formulario.save()
            tarea=get_object_or_404(Tareas, pk=tarea.id)
            tarea.padre=padre
            tarea.save()
            u=Usuarios_Tarea(usuario_id=request.user.id, tarea=tarea, estado=2)
            u.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))

    else:
        formulario=Crear_Tarea(instance=request.user, user=request.user, joinity=joinity)
    context={"formulario":formulario, "joinity":joinity}
    return render_to_response("crear_tarea.html", context, context_instance=RequestContext(request))
def crear_tarea_2(request, joinity_id, tarea_id):
    state = "Invitar usuarios"
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuarios_invitados=[]
    usuarios_tarea=Usuarios_Tarea.objects.filter(tarea=tarea)
    for user in usuarios_tarea:
        usuarios_invitados.append(user.usuario)

    context={"state":state, "joinity": joinity, "tarea": tarea, "usuarios_invitados": usuarios_invitados}
    return render_to_response('crear_tarea_2.html', context, context_instance=RequestContext(request))
def invitar_tarea(request, joinity_id, tarea_id, usuario_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuario=get_object_or_404(User, pk=usuario_id)
    if Usuarios_Tarea.objects.filter(usuario=usuario, tarea=tarea).count()==0:
        nuevo=Usuarios_Tarea(usuario=usuario, tarea=tarea, estado=0)
        nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))
def invitar_todos_tarea(request, joinity_id, tarea_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    usuarios_joinity=Usuarios_Joinity.objects.filter(joinity=joinity)
    for usuario in usuarios_joinity:
        print usuario.usuario.first_name
        if Usuarios_Tarea.objects.filter(usuario=usuario.usuario, tarea=tarea).count()==0:
            nuevo=Usuarios_Tarea(usuario=usuario.usuario, tarea=tarea, estado=0)
            nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/2/"+str(tarea.id))
def crear_tarea_3(request, joinity_id, tarea_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    tarea=get_object_or_404(Tareas, pk=tarea_id)
    state="Anyadir Lugares"
    if request.POST:
        formulario=Anyadir_Lugar_Tarea(request.POST)
        state="Anyadido Lugar"
        if formulario.is_valid:
            n=tarea.lugares_tarea.count()
            n+=1
            nuevo=Lugares_Tarea(tarea=tarea, lugar=request.POST["lugar"], n=n)
            nuevo.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id)+"/tarea/crear/3/"+str(tarea.id))
    else:
        formulario=Anyadir_Lugar_Tarea()
    context={"joinity": joinity, "tarea": tarea,"formulario":formulario, "state": state}
    return render_to_response('crear_tarea_3.html', context, context_instance=RequestContext(request))

def crear_reserva(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    return render_to_response("crear_reserva.html", {"joinity":joinity})

def buscar_restaurante(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    if request.GET:
        busqueda = Buscar_Reserva(request.GET)
        restaurantes = Empresa.objects.filter(nombre=request.GET["s"])
    else:
        busqueda = Buscar_Reserva()
        restaurantes = False
    context={"joinity":joinity, "restaurantes":restaurantes, "busqueda":busqueda}
    return render_to_response('buscar_restaurante.html', context)  # Create your views here.

def buscar_hotel(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    if request.GET:
        busqueda = Buscar_Reserva(request.GET)
        hoteles = Empresa.objects.filter(nombre=request.GET["s"])
    else:
        busqueda = Buscar_Reserva()
        hoteles = False
    context={"joinity":joinity, "hoteles":hoteles, "busqueda":busqueda}
    return render_to_response('buscar_hoteles.html', context)  # Create your views here.

def crear_reserva_restaurante(request, joinity_id, empresa_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    empresa=get_object_or_404(Empresa, pk=empresa_id)
    if request.POST:
        formulario=Reservar(request.POST, family=joinity.family_rel, empresa=empresa)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id))
    else:
        formulario=Reservar(family=joinity.family_rel, empresa=empresa)
    context={"formulario":formulario, "joinity":joinity}
    return render_to_response('crear_reserva_restaurante.html', context, context_instance=RequestContext(request))  # Create your views here.

def crear_reserva_hotel(request, joinity_id, empresa_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    empresa=get_object_or_404(Empresa, pk=empresa_id)
    if request.POST:
        formulario=Reservar(request.POST, family=joinity.family_rel, empresa=empresa)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id))
    else:
        formulario=Reservar(family=joinity.family_rel, empresa=empresa)
    context={"formulario":formulario, "joinity":joinity}
    
    return render_to_response('crear_reserva_hotel.html', context, context_instance=RequestContext(request))  # Create your views here.

def ver_reserva(request, joinity_id, reserva_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    reserva=get_object_or_404(Reservas_Empresas, pk=reserva_id)
    context={"joinity":joinity, "reserva":reserva}
    return render_to_response('ver_reserva.html', context)

@login_required
def invitar_usuario(request, joinity_id, usuario_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    usuario = get_object_or_404(User, pk=usuario_id)
    if not usuario.usuario.invitado_joinity(joinity):
        u = Usuarios_Joinity(usuario_id=usuario.id, joinity_id=joinity.id)
        u.save()
        if not LOCALHOST:
            send_mail('INVITACION A JOINITY ', "Se le ha invitado al joinity\nhttp://prueba1.bueninvento.net/joinity/ver/" + str(joinity.id), 'antoni@bueninvento.es',
                              [usuario.email], fail_silently=False)
    return HttpResponseRedirect(request.GET["next"])

def nombrar_admin(request, usuario_joinity_id):
    usuario_joinity=get_object_or_404(Usuarios_Joinity, pk=usuario_joinity_id)
    if usuario_joinity.estado==1:
        usuario_joinity.estado=2
        usuario_joinity.save()
    return HttpResponseRedirect("/joinity/ver/"+str(usuario_joinity.joinity.id))
def aceptar_membresia(request, usuario_joinity_id):
    usuario_joinity=get_object_or_404(Usuarios_Joinity, pk=usuario_joinity_id)
    if usuario_joinity.estado==-1:
        usuario_joinity.estado=1
        usuario_joinity.save()
    return HttpResponseRedirect("/joinity/ver/"+str(usuario_joinity.joinity.id))


def confirmar(request, reserva_id):
    reserva=get_object_or_404(Reservas_Empresas, pk=reserva_id)
    reserva.estado=1
    reserva.save()
    return HttpResponseRedirect("/joinity/"+str(reserva.family.joinity.id))
def aprobar(request, reserva_id):
    reserva=get_object_or_404(Reservas_Empresas, pk=reserva_id)
    reserva.estado=2
    reserva.save()
    return HttpResponseRedirect("/empresa/"+str(reserva.empresa.id))
def unirse_evento(request, joinity_id, evento_id):
    evento=get_object_or_404(Eventos, pk=evento_id)
    if not Usuarios_Evento.objects.filter(usuario=request.user, evento=evento).exists():
        nuevo=Usuarios_Evento(usuario=request.user, evento=evento, estado=1)
        nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(evento.joinity.id))

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

