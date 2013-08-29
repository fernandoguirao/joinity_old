from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from joinitys.models import Joinitys, Reservas_Joinity
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from models import Brand
from django.core.mail import send_mail
from datetime import datetime
from forms import ReservaRestaurante, ReservaHotel
@dajaxice_register
def cargar_mas(request, brand_id, n, order):
    #lista_aficiones=Joinitys.objects.filter(tipo="3")[n:n+8]
    brand=get_object_or_404(Brand, pk=brand_id)
    if order==1:
        lista_joinitys=Joinitys.objects.filter(tipo=2, compras__brand=brand).order_by("-id")[n:n+8]
    elif order==2:
        lista_joinitys=Joinitys.objects.filter(tipo=2, compras__brand=brand).order_by("precio")[n:n+8]
    elif order==3:
        lista_joinitys=Joinitys.objects.filter(tipo=2, compras__subcategoria__in=request.user.usuario.intereses_compras.all, compras__brand=brand).order_by("-id")[n:n+8]
    joinitys=render_to_string('brands/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()+n
    return simplejson.dumps({'joinitys':joinitys, 'n':n})
@dajaxice_register
def carga_reserva(request, reserva_id):
    reserva=get_object_or_404(Reservas_Joinity, pk=reserva_id)
    context={"reserva":reserva}
    pagina_reserva=render_to_string("brands/mis_reservas/reserva.html", context)
    return simplejson.dumps({"reserva":pagina_reserva})
@dajaxice_register
def confirmar_reserva_empresa(request, reserva_id):
    reserva=get_object_or_404(Reservas_Joinity, pk=reserva_id)
    reserva.estado=2
    reserva.save()
    return simplejson.dumps({'ok':True})
@dajaxice_register
def cancelar_reserva_empresa(request, reserva_id):
    reserva=get_object_or_404(Reservas_Joinity, pk=reserva_id)
    reserva.estado=3
    reserva.save()
    return simplejson.dumps({'ok':False})
@dajaxice_register
def filtrar(request, brand_id, categoria, order):
    brand=get_object_or_404(Brand, pk=brand_id)
    if order==1:
        lista_joinitys=Joinitys.objects.filter(tipo=2, compras__brand=brand).order_by("-id")[:8]
    elif order==2:
        lista_joinitys=Joinitys.objects.filter(tipo=2, compras__brand=brand).order_by("precio")[:8]
    elif order==3:
        lista_joinitys=Joinitys.objects.filter(tipo=2, compras__brand=brand, compras__subcategoria__in=request.user.usuario.intereses_compras.all).order_by("-id")[:8]
    joinitys=render_to_string('brands/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "order":order, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()
    return simplejson.dumps({'joinitys':joinitys, 'n':n, 'order':order})
@dajaxice_register
def seguir(request, brand_id):
    brand=get_object_or_404(Brand, pk=brand_id)
    brand.seguidores.add(request.user)
    return simplejson.dumps({'ok':'ok'})
@dajaxice_register
def dejar_de_seguir(request, brand_id):
    brand=get_object_or_404(Brand, pk=brand_id)
    brand.seguidores.remove(request.user)
    return simplejson.dumps({'ok':'ok'})
@dajaxice_register
def reserva_restaurante(request,formulario, id_brand, joinity_id):
    brand=get_object_or_404(Brand, pk=id_brand)
    if joinity_id!=0:
        joinity=get_object_or_404(Joinitys, pk=joinity_id)
        form=ReservaRestaurante(formulario, joinity=joinity, usuario=request.user, brand=brand)
        reserva=form.save()
        fecha=datetime(reserva.fecha_inicio.year, reserva.fecha_inicio.month, reserva.fecha_inicio.day, int(formulario["hora"]), int(formulario["minuto"]))
        reserva.fecha_inicio=fecha
        reserva.save()

    cadena="El usuario "+request.user.first_name+" "+request.user.last_name+"\n"
    cadena+="con el email "+request.user.email+"\n"
    cadena+="ha solicitado una reserva el dia "+str(formulario["fecha_inicio"])
    cadena+=" a las "+str(formulario["hora"])+":"+str(formulario["minuto"])+"\n"
    cadena+=" con la nota:\n "+formulario["notas"]+"\n"
    cadena+=" de "+str(formulario["n_personas"])+"personas \n"
    send_mail('RESERVA ', cadena, 'joinity@joinity.com',
                  [brand.admin.email], fail_silently=False)
    return simplejson.dumps({'ok':True})
@dajaxice_register
def confirmar_reserva(request, reserva_id):
    reserva=get_object_or_404(Reservas_Joinity, pk=reserva_id)
    reserva.estado=1
    reserva.save()
    return simplejson.dumps({'ok':True})
@dajaxice_register
def reserva_hotel(request,formulario, id_brand, joinity_id):
    brand=get_object_or_404(Brand, pk=id_brand)
    if joinity_id!=0:
        joinity=get_object_or_404(Joinitys, pk=joinity_id)
        form=ReservaHotel(formulario, joinity=joinity, usuario=request.user, brand=brand)
        reserva=form.save()
        fecha=datetime(reserva.fecha_inicio.year, reserva.fecha_inicio.month, reserva.fecha_inicio.day, int(formulario["hora_inicio"]), int(formulario["minuto_inicio"]))
        reserva.fecha_inicio=fecha
        fecha=datetime(reserva.fecha_fin.year, reserva.fecha_fin.month, reserva.fecha_fin.day, int(formulario["hora_fin"]), int(formulario["minuto_fin"]))
        reserva.fecha_fin=fecha
        reserva.save()

    cadena="El usuario "+request.user.first_name+" "+request.user.last_name+"\n"
    cadena+="con el email "+request.user.email+"\n"
    cadena+="ha solicitado una reserva del dia "+str(formulario["fecha_inicio"])
    cadena+=" a las "+str(formulario["hora_inicio"])+":"+str(formulario["minuto_inicio"])+"\n"
    cadena+=" al dia "+str(formulario["fecha_fin"])
    cadena+=" a las "+str(formulario["hora_fin"])+":"+str(formulario["minuto_fin"])+"\n"
    cadena+=" de "+str(formulario["n_personas"])+" personas en "+str(formulario["n_habitaciones"])+" habitaciones\n"
    send_mail('RESERVA ', cadena, 'joinity@joinity.com',
                  [brand.admin.email], fail_silently=False)
    
    return simplejson.dumps({'ok':True})

    