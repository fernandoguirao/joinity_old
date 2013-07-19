from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template.loader import render_to_string

@dajaxice_register
def refrescar(request):
    if request.user.usuario.tiene_notificaciones:
        menu=render_to_string('persistentes/ajax_notificaciones.html', {"usuario":request.user,})
    else:
        menu=False
    return simplejson.dumps({'menu':menu})


