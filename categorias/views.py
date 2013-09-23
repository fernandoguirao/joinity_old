from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect
from forms import NuevoInteresForm, NuevaCompraForm
from django.contrib.auth.models import User
from joinitys.models import Joinitys
from models import Subcategorias
@login_required
def nuevo_interes(request):
    if request.POST:
        formulario = NuevoInteresForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            if request.GET["next"]:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect('/editar/')
    else:
        formulario = NuevoInteresForm(instance=request.user.usuario)
    context = {'formulario':formulario}
    return render_to_response('nuevo_interes.html', context, context_instance=RequestContext(request))  # Create your views here.
def nueva_compra(request):
    if request.POST:
        formulario = NuevaCompraForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/editar/')
    else:
        formulario = NuevaCompraForm(instance=request.user.usuario)
    context = {'formulario':formulario}
    return render_to_response('nuevo_interes.html', context, context_instance=RequestContext(request))  # Create your views here.

def mis_categorias(request):
    mis_categorias=request.user.usuario.intereses.all()
    lista_joinitys=Joinitys.objects.filter(aficiones__subcategoria=mis_categorias[0])
    bloggers=User.objects.filter(usuario__intereses_blog__id=mis_categorias[0].id)
    usuarios=User.objects.filter(usuario__intereses__id=mis_categorias[0].id, usuario_amigos__amigo__id=request.user.id)
    context={'mis_categorias':mis_categorias, 'usuarios':usuarios, 'bloggers':bloggers, 'lista_joinitys':lista_joinitys, "usuario":request.user, "pagina":"misAficioens","cinco":[1,2,3,4,5]}
    return render(request, 'joinitys/misAficiones/misjoinitys.html', context)
