from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from forms import NuevoInteresForm, NuevaCompraForm
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
