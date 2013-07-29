from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from models import Brand
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from forms import BrandForm, ReservaRestaurante, ReservaHotel
from joinitys.models import Joinitys


def ver(request, id_brand=False):
    brand=get_object_or_404(Brand, pk=id_brand)
    joinitys=Joinitys.objects.filter(tipo="2", compras__brand=brand).order_by('-id')[:8]
    seguidor=Brand.objects.filter(pk=brand.id, seguidores__id=request.user.id).exists()
    reserva_restaurante=ReservaRestaurante()
    reserva_hotel=ReservaHotel()
    context={"usuario":request.user, "pagina":"brands", "brand":brand, "joinitys":joinitys, 
             "seguidor":seguidor, "reserva_restaurante":reserva_restaurante, "reserva_hotel":reserva_hotel}
    return render_to_response('brands/single/index.html', context,context_instance=RequestContext(request))
def editar(request, id_brand):
    brand=get_object_or_404(Brand, pk=id_brand)
    if request.user!=brand.admin:
        return HttpResponse("No tienes permisos para ver esto.")
    if request.method == 'POST':
        formulario=BrandForm(request.POST, request.FILES, instance=brand)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario=BrandForm(instance=brand)
    context={"formulario":formulario, "usuario":request.user}
    return render_to_response('brands/single/edit.html', context, context_instance=RequestContext(request))


def seguir_empresa(request, empresa_id):
    empresa=get_object_or_404(Brand, pk=empresa_id)
    empresa.seguidores.add(request.user)
    return HttpResponseRedirect("/empresa/"+str(empresa.id))
