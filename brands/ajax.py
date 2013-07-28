from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from joinitys.models import Joinitys
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from models import Brand


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

    