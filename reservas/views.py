from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from models import Empresa, Fotos_Empresa, Puntuaciones
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from forms import EmpresaForm, Subir_Foto, Puntuar

def editar_reserva(request, empresa_id):
    empresa=get_object_or_404(Empresa, pk=empresa_id)
    param_foto=request.GET.get("foto", 0)

    if empresa.admin!=request.user:
        return HttpResponse("No tienes permisos para ver esto.")
    if request.method == 'POST':
        # formulario enviado
        if param_foto==0:
            empresaform = EmpresaForm(request.POST, request.FILES, instance=empresa)
            subir_foto=Subir_Foto(instance=request.user, empresa=empresa, prefix='subir_foto')
            if empresaform.is_valid():
                empresaform.save()
                return HttpResponseRedirect("/empresa/"+str(empresa.id))

        else:
            subir_foto=Subir_Foto(request.POST, request.FILES, empresa=empresa, prefix='subir_foto')
            empresaform = EmpresaForm(instance=empresa)
            if subir_foto.is_valid():
                subir_foto.save()


    else:
        # formulario inicial
        empresaform = EmpresaForm(instance=empresa)
        subir_foto=Subir_Foto(instance=request.user, empresa=empresa, prefix='subir_foto')
    context={'empresaform': empresaform, "subir_foto": subir_foto, "empresa":empresa}
    return render_to_response('editar_empresa.html', context, context_instance=RequestContext(request))

def ver_empresa(request, empresa_id):
    empresa=get_object_or_404(Empresa, pk=empresa_id)
    if request.POST:
        puntuar=Puntuar(request.POST, empresa=empresa, usuario=request.user)
        if Puntuaciones.objects.filter(empresa=empresa, usuario=request.user).exists():
            puntuacion=get_object_or_404(Puntuaciones, empresa=empresa, usuario=request.user)
            puntuacion.delete()
        if puntuar.is_valid():
            puntuar.save()
    else:
        puntuar=Puntuar(empresa=empresa, usuario=request.user)
    context={'empresa':empresa, 'puntuar':puntuar, 'usuario':request.user}
    return render_to_response('ver_empresa.html', context,context_instance=RequestContext(request))

def seguir_empresa(request, empresa_id):
    empresa=get_object_or_404(Empresa, pk=empresa_id)
    empresa.seguidores.add(request.user)
    return HttpResponseRedirect("/empresa/"+str(empresa.id))
