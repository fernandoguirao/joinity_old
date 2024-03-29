from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import FormTexto, FormFoto, FormVotacion
from forms import Buscar as Buscar_Reserva, Reservar, FormComentario
from django.contrib.auth.decorators import login_required
from models import Reserva_Brand, Joinitys, Joinitys_VIP, Compras, Aficiones, Usuarios_Joinity, Puntuaciones
from django.http import HttpResponseRedirect
from django.shortcuts import  render, get_object_or_404
from django.contrib.auth.models import User
from joinity.settings import LOCALHOST
from django.core.mail import send_mail
from brands.models import Brand
from joinitys.eventos.models import Eventos, Usuarios_Evento
from joinitys.pagos.forms import PagosForm
from notificaciones.models import Notificaciones
from categorias.models import Subcategorias_Compras, Categorias_Compras, Subcategorias, Categorias
from joinitys.tareas.models import Tareas
from joinitys.pagos.models import Usuarios_Pagos
def index(request):
    if not request.user.is_authenticated():
        usuario=False
    else:
        usuario=request.user
        if not request.user.first_name:
            return HttpResponseRedirect('/usuario/editar/')
    # lista_pagos = Pagos.objects.filter(usuarios=request.user.id).order_by('id')
    #lista_joinitys = Usuarios_Joinity.objects.filter(usuario=request.user)
    lista_aficiones=Joinitys.objects.filter(tipo="3").order_by('-id')[:8]
    lista_compras=Joinitys.objects.filter(tipo="2").order_by('-id')[:8]
    lista_family=Joinitys.objects.filter(tipo="1").order_by('-id')[:8]
    lista_vip=Joinitys_VIP.objects.all()
    lista_restaurantes=Brand.objects.filter(clase="2")
    lista_hoteles=Brand.objects.filter(clase="1")
    context = {'lista_aficiones': lista_aficiones, 'lista_compras':lista_compras,
               'lista_family':lista_family, "usuario":usuario, "pagina":"home",
               "cinco":[1,2,3,4,5], "VIP":lista_vip, "send":request.GET.get("send",False),
               "error":request.GET.get("error", False), "lista_restaurantes":lista_restaurantes,
               "lista_hoteles":lista_hoteles}
    return render(request, 'index/index.html', context)



@login_required
def mis_joinitys(request):
    lista_joinitys=Usuarios_Joinity.objects.filter(usuario=request.user)
    context={'lista_joinitys':lista_joinitys, "usuario":request.user, "pagina":"misJoinitys","cinco":[1,2,3,4,5]}
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
def ver(request, joinity_id):
    # What you want the button to do.
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    
    if Notificaciones.objects.filter(usuario=request.user, tipo=1, id_notificacion=joinity.id).exists():
        notificacion=Notificaciones.objects.get(usuario=request.user, tipo=1, id_notificacion=joinity.id)
        notificacion.estado=1
        notificacion.save()
    
    soy=joinity.que_soy(request.user)
    frmpago=PagosForm(joinity=joinity, user=request.user)
    mis_tareas=Tareas.objects.filter(joinity=joinity, usuarios_tarea__usuario=request.user)
    if Puntuaciones.objects.filter(usuario=request.user, joinity=joinity).exists():
        puntuacion_media=int(joinity.puntuacion_media())
    else:
        puntuacion_media=0
    if joinity.tipo==1:
        lista_compras=Joinitys.objects.filter(tipo=2)
        lista_hoteles=Brand.objects.filter(clase=1)
        lista_restaurantes=Brand.objects.filter(clase=2)
    else:
        lista_compras=False
        lista_hoteles=False
        lista_restaurantes=False
    if request.POST:
        form = FormFoto(request.POST, request.FILES, joinity=joinity, usuario=request.user)
        comentar=FormComentario(instance=request.user, usuario=request.user, actualizacion=0)
        votacionform=FormVotacion(usuario=request.user, joinity=joinity)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect("/joinity/"+str(joinity.id))
    else:
        form = FormTexto(instance=request.user, usuario=request.user, joinity=joinity)
        comentar=FormComentario(instance=request.user, usuario=request.user, actualizacion=0)
        votacionform=FormVotacion(usuario=request.user, joinity=joinity)
    context = {"joinity": joinity, "form": form, "cinco":[1,2,3,4,5],
               "pagina":"joinity", "comentar":comentar, "lista_compras":lista_compras,
               "lista_hoteles":lista_hoteles, "lista_restaurantes":lista_restaurantes,
               "puntuacion":puntuacion_media, "frmpago":frmpago,
               "usuario":request.user, "soy":soy, "mis_tareas":mis_tareas, "formvotacion":votacionform}
    return render_to_response("single/joinity.html", context, context_instance=RequestContext(request))


def aceptar(request, joinity_id):
    usuario_joinity=get_object_or_404(Usuarios_Joinity, joinity=joinity_id, usuario=request.user)
    if usuario_joinity.estado==0:
        usuario_joinity.estado=1
        usuario_joinity.save()
    return HttpResponseRedirect("/joinity/"+str(usuario_joinity.joinity.id))


def unirse(request, joinity_id):
    if request.user.is_authenticated():
        joinity = get_object_or_404(Joinitys, pk=joinity_id)
        if joinity.privacidad==0:
            nuevo=Usuarios_Joinity(joinity=joinity, usuario=request.user, estado=1)
            nuevo.save()
        elif joinity.privacidad==1:
            nuevo=Usuarios_Joinity(joinity=joinity, usuario=request.user, estado=-1)
            nuevo.save()
        return HttpResponseRedirect("/joinity/"+str(joinity.id))
    return HttpResponseRedirect("/")




def crear_reserva(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    return render_to_response("crear_reserva.html", {"joinity":joinity})

def buscar_restaurante(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    if request.GET:
        busqueda = Buscar_Reserva(request.GET)
        restaurantes = Brand.objects.filter(nombre=request.GET["s"])
    else:
        busqueda = Buscar_Reserva()
        restaurantes = False
    context={"joinity":joinity, "restaurantes":restaurantes, "busqueda":busqueda}
    return render_to_response('buscar_restaurante.html', context)  # Create your views here.

def buscar_hotel(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    if request.GET:
        busqueda = Buscar_Reserva(request.GET)
        hoteles = Brand.objects.filter(nombre=request.GET["s"])
    else:
        busqueda = Buscar_Reserva()
        hoteles = False
    context={"joinity":joinity, "hoteles":hoteles, "busqueda":busqueda}
    return render_to_response('buscar_hoteles.html', context)  # Create your views here.

def crear_reserva_restaurante(request, joinity_id, empresa_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    empresa=get_object_or_404(Brand, pk=empresa_id)
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
    empresa=get_object_or_404(Brand, pk=empresa_id)
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
    reserva=get_object_or_404(Reserva_Brand, pk=reserva_id)
    context={"joinity":joinity, "reserva":reserva}
    return render_to_response('ver_reserva.html', context)

@login_required
def invitar_usuario(request, joinity_id, usuario_id):
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    usuario = get_object_or_404(User, pk=usuario_id)
    if not usuario.usuario.invitado_joinity(joinity):
        u = Usuarios_Joinity(usuario_id=usuario.id, joinity_id=joinity.id)
        u.save()
        notificacion=Notificaciones(usuario=usuario, tipo=1, id_notificacion=joinity.id)
        notificacion.save()
        if not LOCALHOST:
            send_mail('INVITACION A JOINITY ', "Se le ha invitado al joinity\nhttp://joinity.net/joinity/ver/" + str(joinity.id), 'joinity@joinity.com',
                              [usuario.email], fail_silently=False)
    return HttpResponseRedirect(request.GET["next"])

def nombrar_admin(request, usuario_joinity_id):
    usuario_joinity=get_object_or_404(Usuarios_Joinity, pk=usuario_joinity_id)
    if usuario_joinity.estado==1:
        usuario_joinity.estado=2
        usuario_joinity.save()
    return HttpResponseRedirect("/joinity/"+str(usuario_joinity.joinity.id))
def aceptar_membresia(request, usuario_joinity_id):
    usuario_joinity=get_object_or_404(Usuarios_Joinity, pk=usuario_joinity_id)
    if usuario_joinity.estado==-1:
        usuario_joinity.estado=1
        usuario_joinity.save()
    return HttpResponseRedirect("/joinity/"+str(usuario_joinity.joinity.id))


def confirmar(request, reserva_id):
    reserva=get_object_or_404(Reserva_Brand, pk=reserva_id)
    reserva.estado=1
    reserva.save()
    return HttpResponseRedirect("/joinity/"+str(reserva.family.joinity.id))
def aprobar(request, reserva_id):
    reserva=get_object_or_404(Reserva_Brand, pk=reserva_id)
    reserva.estado=2
    reserva.save()
    return HttpResponseRedirect("/empresa/"+str(reserva.empresa.id))
def unirse_evento(request, joinity_id, evento_id):
    evento=get_object_or_404(Eventos, pk=evento_id)
    if not Usuarios_Evento.objects.filter(usuario=request.user, evento=evento).exists():
        nuevo=Usuarios_Evento(usuario=request.user, evento=evento, estado=1)
        nuevo.save()
    return HttpResponseRedirect("/joinity/"+str(evento.joinity.id))
@login_required
def abandonar(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    if not joinity.soy_admin(request.user):
        Usuarios_Joinity.objects.filter(joinity=joinity, usuario=request.user).delete()
    else:
        if joinity.creador!=request.user:
            Usuarios_Joinity.objects.filter(joinity=joinity, usuario=request.user).delete()
        else:
            Usuarios_Joinity.objects.filter(joinity=joinity).delete()
            Joinitys.objects.filter(joinity=joinity).delete()
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("/joinity/"+str(joinity.id))

def comprar(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    Usuarios_Pagos.objects.get_or_create(usuario=request.user, pago=joinity.pagos.all()[0])
    return HttpResponseRedirect("/mis_compras/")

                



