from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from forms import NuevoInteresForm, NuevaCompraForm
from django.template.loader import render_to_string
from joinitys.models import Joinitys
from django.contrib.auth.models import User
@dajaxice_register   
def crear(request, formulario, tipo):
    if tipo==1:
        formulario=NuevoInteresForm(formulario)
        if formulario.is_valid():
            formulario.save()
            return simplejson.dumps({'ok': True})
    elif tipo==2:
        formulario=NuevaCompraForm(formulario)
        if formulario.is_valid():
            formulario.save()
            return simplejson.dumps({'ok': True})
    return simplejson.dumps({'ok':False})
@dajaxice_register
def cargar_joinitys(request, categoria_id):
    lista_joinitys=Joinitys.objects.filter(aficiones__subcategoria_id=categoria_id)
    bloggers=User.objects.filter(usuario__intereses_blog__id=categoria_id)
    usuarios=User.objects.filter(usuario__intereses__id=categoria_id, usuario_amigos__amigo__id=request.user.id)
    context={"lista_joinitys":lista_joinitys, 'bloggers': bloggers, 'usuarios':usuarios, "cinco":[1,2,3,4,5]}
    joinitys=render_to_string('joinitys/misAficiones/ajax_mis_joinitys.html', context)
    if joinitys:
        return simplejson.dumps({'error':False, 'joinitys':joinitys})
    else:
        return simplejson.dumps({'error':True})
