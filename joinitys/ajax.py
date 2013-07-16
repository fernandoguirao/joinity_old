from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from joinitys.models import Joinitys
from django.template.loader import render_to_string
@dajaxice_register
def cargar_mas(request, categoria, n):
    #lista_aficiones=Joinitys.objects.filter(tipo="3")[n:n+8]
    lista_joinitys=Joinitys.objects.filter(tipo=categoria)[n:n+8]
    aficiones=render_to_string('index/ajax_lista_joinitys.html', {"lista_joinitys":lista_joinitys, "cinco":[1,2,3,4,5]})
    n=lista_joinitys.count()+n
    return simplejson.dumps({'aficiones':aficiones, 'n':n})

