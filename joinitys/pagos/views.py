from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import PagosForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from models import Pagos, Usuarios_Pagos
from django.http import HttpResponseRedirect
from joinity.settings import LOCALHOST
from django.core.mail import send_mail
from django.contrib.auth.models import User
from joinitys.models import Joinitys
from datetime import datetime
@login_required
def crear(request, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    state = "Crea Pago aqui..."
    if request.POST:
        state = "Creado pago"
        formulario = PagosForm(request.POST, user=request.user, joinity=joinity)
        if formulario.is_valid:
            n = 0
            pago = formulario.save()
            for usuario in request.POST.getlist('usuarios'):
                n = n + 1
                u = Usuarios_Pagos(usuario_id=usuario, pago_id=pago.id)
                u.save()
                if not LOCALHOST:
                    send_mail('ASIGNACION DE PAGO ', "Se le ha asignado el pago con el concepto " + str(pago.concepto), 'joinity@joinity.com',
                              [User.objects.get(id=usuario).email], fail_silently=False)
            return HttpResponseRedirect('/joinity/'+str(joinity.id))
    else:
        formulario = PagosForm(user=request.user, joinity=joinity)
    context={'state':state, 'formulario':formulario, 'usuario':request.user, 'joinity':joinity}
    return render_to_response('joinitys/pagos/crear.html', context, context_instance=RequestContext(request))

@login_required
def cancelar(request, joinity_id, pago_id):
    pago=get_object_or_404(Pagos, pk=pago_id)
    Usuarios_Pagos.objects.get(pago=pago, usuario=request.user).delete()
    return HttpResponseRedirect('/joinity/'+str(joinity_id))

@login_required
def mis_pagos(request):
    mis_pagos=Pagos.objects.filter(usuarios__usuario=request.user)
    mis_compras=Pagos.objects.filter(joinity__joinity_usuario__usuario=request.user, joinity__tipo=2).exclude(usuarios__usuario=request.user)
    context={"pagina":"misCompras", "usuario":request.user, "lista_pagos":mis_pagos, "lista_compras":mis_compras}
    return render_to_response("joinitys/pagos/mis_pagos.html", context)
