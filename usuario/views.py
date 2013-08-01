# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404
from amigos.models import Amigos
from django.template import RequestContext
from models import Usuarios, Puntuaciones
from datetime import datetime
from forms import Puntuar, Buscar, PerfilForm, UserForm, UserCreateForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from joinity.settings import LOCALHOST
from categorias.models import Categorias_Compras, Subcategorias

@login_required
def ver_perfil(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    logeado = request.user.id == usuario.id;
    son_amigos = usuario.usuario.son_amigos(request.user.id)
    solicitud=usuario.usuario.solicitud_amistad(request.user.id)
    lista_amigos = Amigos.objects.filter(usuario=request.user, estado=1)
    if request.POST:
        formulario = Puntuar(request.POST, puntuador=request.user, puntuado=usuario)
        if Puntuaciones.objects.filter(puntuador=request.user, usuario=usuario).exists():
            puntuacion = get_object_or_404(Puntuaciones, puntuador=request.user, usuario=usuario)
            puntuacion.delete()
        if formulario.is_valid:
            formulario.save()
    else:
        formulario = Puntuar(instance=request.user, puntuador=request.user, puntuado=usuario)
    context = {'perfil': usuario, 'logeado':logeado, 'solicitud':solicitud,'amigos':son_amigos, 'lista_amigos':lista_amigos, 'formulario':formulario, "pagina":"ver", "usuario":request.user}
    return render_to_response('usuario/perfil.html', context, context_instance=RequestContext(request))  # Create your views here.
def mi_perfil(request):
    usuario = get_object_or_404(User, pk=request.user.id)
    logeado = request.user.id == usuario.id;
    lista_amigos = Amigos.objects.filter(usuario=request.user, estado=1)
    busqueda = Buscar()
    context = {'perfil': usuario, 'logeado':logeado, 'lista_amigos':lista_amigos, 'busqueda':busqueda, "pagina":"ver", "usuario":request.user}
    return render_to_response('usuario/perfil.html', context)  # Create your views here.
def busqueda(request):
    state = ""
    if request.GET["filtro"] == '1':
        usuarios = User.objects.filter(first_name=request.GET["input"])
    elif request.GET["filtro"] == '2':
        users = Usuarios.objects.filter(ciudad=request.GET["input"])
        usuarios = []
        for user in users:
            usuarios.append(user.usuario)
    elif request.GET["filtro"] == '3':
        usuarios = []
        
        fecha = datetime.strptime(request.GET["input"], '%d/%m/%Y')
        users = Usuarios.objects.filter(nacimiento=fecha)
        for user in users:
            usuarios.append(user.usuario)
    elif request.GET["filtro"] == '4':
        usuarios = User.objects.filter(email=request.GET["input"])
    elif request.GET["filtro"] == '5':
        users = Usuarios.objects.all()
        usuarios = []
        for user in users:
            for _ in user.intereses.filter(nombre=request.GET["input"]):
                usuarios.append(user.usuario)
                    
    else:
        usuarios = False
    context = {'usuarios': usuarios, 'state':state }
    return render_to_response('busqueda.html', context)  # Create your views here.

def mandarmail(request):
    send_mail('PAGO', 'Se confirma el pago.', 'antoni@bueninvento.es',
    ["antoniespinosa@me.com"], fail_silently=False)
    return HttpResponseRedirect('/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_user(request):
    pagina="login"
    state=False
    if request.POST:
        formulario = AuthenticationForm(request.POST)
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                if(request.GET.get("next", 0)!=0):
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponseRedirect('/')
            else:
                state="Error: Tu cuenta no ha sido activa, espera a que un administrador la active"
        else:
            state="Error: Contraseña incorrecta"

    else:
        formulario = AuthenticationForm()
    context={'pagina':pagina, 'formulario': formulario, "state":state}
    return render_to_response('login/login.html', context, context_instance=RequestContext(request))
    
def registro(request):
    if request.method == 'POST':
        formulario = UserCreateForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            u = User.objects.get(username=request.POST['username'])
            u.is_active=False
            u.save()
            usuario = Usuarios(usuario=u)
            usuario.save()
            return HttpResponseRedirect('/usuario/editar/')
    else:
        formulario = UserCreateForm()
    context={"formulario":formulario}
    return render_to_response('usuario/registro.html', context, context_instance=RequestContext(request))
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # formulario enviado
        user_form = UserForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=request.user.usuario)

        if user_form.is_valid() and perfil_form.is_valid():
            # formulario validado correctamente
            user_form.save()
            perfil_form.save()
            return HttpResponseRedirect('/usuario/')

    else:
        # formulario inicial
        user_form = UserForm(instance=request.user)
        perfil_form = PerfilForm(instance=request.user.usuario)
    context={ 'user_form': user_form, 'perfil_form': perfil_form, "pagina":"editar" , "usuario":request.user, 
             "subcategorias":Subcategorias.objects.all().order_by("categoria"), "categorias_compras":Categorias_Compras.objects.all()}
    return render_to_response('usuario/perfil.html', context, context_instance=RequestContext(request))
def solicitar(request):
    nombre=request.GET.get("solicitaNombre", "")
    mail=request.GET.get("solicitaCorreo", "")
    if nombre=="" or mail=="":
        return HttpResponseRedirect('/?send=2&error=Hay campos vacios')
    elif not LOCALHOST:
        try:
            send_mail("SOLICITUD JOINITY", "El usuario "+str(nombre) +" y mail "+ str(mail) +" Solicita permanencia", "joinity@joinity.com", ["golpesbajos@gmail.com", "borjadegregor@hotmail.com", "antoniespinosa@me.com"], fail_silently=False)
        except Exception as detail:
            return HttpResponseRedirect('/?send=2&error='+detail)
        return HttpResponseRedirect('/?send=1')
    else:
        return HttpResponseRedirect('/?send=2&error=Localhost')
        
