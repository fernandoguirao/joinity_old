from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import NuevoInteresForm, NuevaCompraForm
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
    context={}
    return render_to_response('mis_categorias.html', context)
