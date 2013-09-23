from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from models import Brand
from django.template import RequestContext
from django.shortcuts import  get_object_or_404
from forms import BrandForm, ReservaRestaurante, ReservaHotel, Ubicacion_Brand
from joinitys.models import Joinitys


def ver(request, id_brand=False, joinity_id=0):
    brand=get_object_or_404(Brand, pk=id_brand)
    joinitys=Joinitys.objects.filter(tipo="2", compras__brand=brand).order_by('-id')[:8]
    seguidor=Brand.objects.filter(pk=brand.id, seguidores__id=request.user.id).exists()
    reserva_restaurante=ReservaRestaurante(usuario=request.user, joinity=None, brand=brand)
    reserva_hotel=ReservaHotel(usuario=request.user, joinity=None, brand=brand)
    context={"usuario":request.user, "pagina":"brands", "brand":brand, "joinitys":joinitys, "joinity_origen":joinity_id,
             "seguidor":seguidor, "reserva_restaurante":reserva_restaurante, "reserva_hotel":reserva_hotel}
    return render_to_response('brands/single/index.html', context,context_instance=RequestContext(request))
def editar(request, id_brand):
    brand=get_object_or_404(Brand, pk=id_brand)
    if request.user!=brand.admin:
        return HttpResponse("No tienes permisos para ver esto.")
    if request.method == 'POST':
        formulario=BrandForm(request.POST, request.FILES, instance=brand)
        formulario_ubicaciones=Ubicacion_Brand(request.POST, brand=brand)
        if formulario.is_valid():
            formulario.save()
            if formulario_ubicaciones.is_valid():
                formulario_ubicaciones.save()
    else:
        formulario=BrandForm(instance=brand)
        formulario_ubicaciones=Ubicacion_Brand(brand=brand, instance=brand.ubicaciones.all()[0])
    context={"formulario":formulario, "usuario":request.user, "ubicaciones": formulario_ubicaciones}
    return render_to_response('brands/single/edit.html', context, context_instance=RequestContext(request))

def mis_reservas(request):
    
    context={"pagina":"misReservas", "usuario":request.user}
    return render_to_response('brands/mis_reservas/index.html', context)

def seguir_empresa(request, empresa_id):
    empresa=get_object_or_404(Brand, pk=empresa_id)
    empresa.seguidores.add(request.user)
    return HttpResponseRedirect("/empresa/"+str(empresa.id))
