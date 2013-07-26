from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from categorias.models import Subcategorias, Subcategorias_Compras
from django.shortcuts import  get_object_or_404
from joinitys.models import Joinitys
from joinitys.models import Lugares_Joinity
@dajaxice_register
def cargar_subcategoria(request, categoria, tipo):
    if tipo==1:
        lista_subcategorias=Subcategorias.objects.filter(categoria_id=categoria).order_by('id')
    elif tipo==2:
        lista_subcategorias=Subcategorias_Compras.objects.filter(categoria_id=categoria).order_by('id')
    context={"subcategorias":lista_subcategorias}
    select=render_to_string('creacion/ajax_subcategorias.html', context)
    return simplejson.dumps({'select':select})

@dajaxice_register
def anyadir_lugar(request, lugar, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    n=joinity.lugares.count()
    n+=1
    nuevo=Lugares_Joinity(joinity=joinity, lugar=lugar, n=n)
    nuevo.save()
    context={"joinity":joinity}
    lista=render_to_string('creacion/ajax_lista_lugares.html', context)
    return simplejson.dumps({'lista':lista})

