from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from joinitys.models import Joinitys
from django.template.loader import render_to_string
@dajaxice_register
def cargar_mas(request, categoria, n, order):
    #lista_aficiones=Joinitys.objects.filter(tipo="3")[n:n+8]
    if order==1:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("-id")[n:n+8]
    elif order==2:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("-precio")[n:n+8]
    elif order==3:
        if categoria==3:
            #Si es aficiones
            lista_joinitys=Joinitys.objects.filter(tipo=categoria, aficiones__in=request.user.intereses)
        elif categoria==2:
            lista_joinitys=Joinitys.objects.filter(tipo=categoria, aficiones__in=request.user.intereses_compras)
    joinitys=render_to_string('index/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()+n
    return simplejson.dumps({'joinitys':joinitys, 'n':n})

@dajaxice_register
def filtar(request, categoria, order):
    if order==1:
        lista_joinitys=Joinitys.objects.filter(tipo=categoria).order_by("-id")[:8]
    aficiones=render_to_string('index/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()
    return simplejson.dumps({'aficiones':aficiones, 'n':n, 'order':order})
    