from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from models import Joinitys
from django.template.loader import render_to_string
from forms import FormTexto, FormFoto
from django.shortcuts import get_object_or_404

@dajaxice_register
def cargar_mas(request, categoria, n, order):
    #lista_aficiones=Joinitys.objects.filter(tipo="3")[n:n+8]
    if order==1:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("-id")[n:n+8]
    elif order==2:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("precio")[n:n+8]
    elif order==3:
        if categoria==3:
            lista_joinitys=Joinitys.objects.filter(tipo=categoria, aficiones__subcategoria__in=request.user.usuario.intereses.all).order_by("-id")[n:n+8]
        elif categoria==2:
            lista_joinitys=Joinitys.objects.filter(tipo=categoria, compras__subcategoria__in=request.user.usuario.intereses_compras.all).order_by("-id")[n:n+8]
    joinitys=render_to_string('index/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()+n
    return simplejson.dumps({'joinitys':joinitys, 'n':n, 'categoria':categoria})

@dajaxice_register
def filtrar(request, categoria, order):
    if order==1:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("-id")[:8]
    elif order==2:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("precio")[:8]
    elif order==3:
        if categoria==3:
            lista_joinitys=Joinitys.objects.filter(tipo=categoria, aficiones__subcategoria__in=request.user.usuario.intereses.all).order_by("-id")[:8]
        elif categoria==2:
            lista_joinitys=Joinitys.objects.filter(tipo=categoria, compras__subcategoria__in=request.user.usuario.intereses_compras.all).order_by("-id")[:8]
    joinitys=render_to_string('index/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "order":order, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()
    return simplejson.dumps({'joinitys':joinitys, 'n':n, 'order':order, 'categoria':categoria})

@dajaxice_register
def postear(request, formulario, joinity_id):
    print "esto es ajax"
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    form = FormTexto(formulario, usuario=request.user, joinity=joinity)
    if form.is_valid():
        form.save()
        return simplejson.dumps({'status':False, 'joinity_id':joinity_id})
    return simplejson.dumps({'status': 'Error al enviar'})


    


    