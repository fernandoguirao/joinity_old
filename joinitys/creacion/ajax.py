from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from categorias.models import Subcategorias, Subcategorias_Compras

@dajaxice_register
def cargar_subcategoria(request, categoria, tipo):
    if tipo==1:
        lista_subcategorias=Subcategorias.objects.filter(categoria_id=categoria).order_by('id')
    elif tipo==2:
        lista_subcategorias=Subcategorias_Compras.objects.filter(categoria_id=categoria).order_by('id')
    context={"subcategorias":lista_subcategorias}
    select=render_to_string('creacion/ajax_subcategorias.html', context)
    return simplejson.dumps({'select':select})
