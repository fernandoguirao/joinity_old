from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from joinitys.models import Joinitys
from django.template.loader import render_to_string
@dajaxice_register
def cargar_mas(request, categoria, n):
    lista_aficiones=Joinitys.objects.filter(tipo="3")
    aficiones=render_to_string('index/ajax_aficiones.html', {"lista_aficiones":lista_aficiones, "cinco":[1,2,3,4,5]})
    return simplejson.dumps({'aficiones':aficiones, 'n':str(n)})

