from datetime import datetime
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from usuario.forms import Buscar
from usuario.models import Usuarios
from joinitys.models import Usuarios_Joinity, Joinitys, Lugares_Joinity
from forms import JoinityForm, FamilyForm, ComprasForm, AficionesForm, Anyadir_Lugar
from categorias.models import Categorias, Categorias_Compras

@login_required
def nuevo_joinity(request):
    context={"usuario":request.user}
    return render_to_response("creacion/index.html", context)
    

@login_required
def nuevo_family(request):
    if request.POST:
        formulario = JoinityForm(request.POST, request.FILES, user=request.user, tipo=1)
        if formulario.is_valid:
            joinity = formulario.save()
            formfamily=FamilyForm(request.POST, joinity=joinity)
            if formfamily.is_valid:
                formfamily.save()
                usuario=Usuarios_Joinity(joinity_id=joinity.id, usuario=request.user, estado=2)
                usuario.save()
            return HttpResponseRedirect("/joinity/nuevo_joinity/family/2/"+str(joinity.id))
    else:
        formulario = JoinityForm(instance=request.user.usuario, user=request.user, tipo=1)
        formfamily=FamilyForm(joinity=None)
    context={'formulario': formulario, 'formfamily':formfamily, "pagina":"crear", "usuario":request.user}
    return render_to_response('creacion/pagina_creacion.html', context, context_instance=RequestContext(request))

@login_required
def nuevo_compras(request):
    if request.user.id not in [1,28,39]:
        return render_to_response('creacion/solicitar_compra.html', {"usuario": request.user})
    if request.POST:
        formulario = JoinityForm(request.POST, request.FILES, user=request.user, tipo=2)
        if formulario.is_valid:
            joinity = formulario.save()
            formcompras=ComprasForm(request.POST, joinity=joinity)
            if formcompras.is_valid:
                formcompras.save()
                usuario=Usuarios_Joinity(joinity_id=joinity.id, usuario=request.user, estado=2)
                usuario.save()
            return HttpResponseRedirect("/joinity/nuevo_joinity/compras/2/"+str(joinity.id))
    else:
        formulario = JoinityForm(instance=request.user.usuario, user=request.user, tipo=2)
        formcompras=ComprasForm(joinity=None)
    context={ 'formulario': formulario, 'formcompras':formcompras, "pagina":"crear", "usuario":request.user, "categorias":Categorias_Compras.objects.all().order_by('id')}
    return render_to_response('creacion/pagina_creacion.html',context , context_instance=RequestContext(request))


@login_required
def nuevo_aficiones(request):
    if request.POST:
        formulario = JoinityForm(request.POST, request.FILES, user=request.user, tipo=3)
        if formulario.is_valid:
            joinity = formulario.save()
            formaficiones=AficionesForm(request.POST, joinity=joinity)
            if formaficiones.is_valid:
                formaficiones.save()
                usuario=Usuarios_Joinity(joinity_id=joinity.id, usuario=request.user, estado=2)
                usuario.save()
            return HttpResponseRedirect("/joinity/nuevo_joinity/aficiones/2/"+str(joinity.id))
    else:
        formulario = JoinityForm(user=request.user, tipo=3)
        formaficiones=AficionesForm(joinity=None)
    context={'formulario': formulario, 'formaficiones':formaficiones, "pagina":"crear", "usuario":request.user, "categorias":Categorias.objects.all().order_by('id')}
    return render_to_response('creacion/pagina_creacion.html', context, context_instance=RequestContext(request))

@login_required
def crear_2(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    if request.POST:
        formulario=Anyadir_Lugar(request.POST)
        if formulario.is_valid:
            n=joinity.lugares.count()
            n+=1
            nuevo=Lugares_Joinity(joinity=joinity, lugar=request.POST["lugar"], n=n)
            nuevo.save()
            return HttpResponseRedirect("/joinity/nuevo_joinity/"+str(joinity.get_tipo())+"/2/"+str(joinity.id))
    else:
        formulario=Anyadir_Lugar()
    context={"joinity": joinity, "formulario":formulario,"pagina":"lugares", "usuario":request.user}
    return render_to_response('creacion/pagina_creacion.html', context, context_instance=RequestContext(request))

@login_required
def crear_3(request, joinity_id):
    busqueda = Buscar()
    joinity = get_object_or_404(Joinitys, pk=joinity_id)
    if request.GET:
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
                if user.intereses.filter(nombre=request.GET["input"]):
                    usuarios.append(user.usuario)
                        
        else:
            usuarios = False

    else:
        usuarios=False
    usuarios_invitados=[]
    usuarios_joinity=Usuarios_Joinity.objects.filter(joinity=joinity)
    for user in usuarios_joinity:
        usuarios_invitados.append(user.usuario)
    context={'busqueda': busqueda, "usuarios":usuarios, "joinity": joinity,
            "usuarios_invitados": usuarios_invitados, "pagina":"invitar", "usuario":request.user}
    return render_to_response('creacion/pagina_creacion.html', context, context_instance=RequestContext(request))