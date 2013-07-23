from django.shortcuts import render_to_response
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from forms import PagosForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, get_object_or_404
from models import Pagos, Usuarios_Pagos
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from joinity.settings import LOCALHOST
from django.core.mail import send_mail
from django.contrib.auth.models import User

@csrf_exempt
@require_POST
def confirmado(request):
    return HttpResponse("CONFIRMADO")

@login_required
def index(request):
    if not request.user.first_name:
        return HttpResponseRedirect('/editar/')
    # lista_pagos = Pagos.objects.filter(usuarios=request.user.id).order_by('id')
    lista_pagos = Usuarios_Pagos.objects.filter(usuario=request.user).order_by('pago')
    context = {'lista_pagos': lista_pagos}
    return render(request, 'index.html', context)

@login_required
def crear_pagos(request):
    state = "Crea Pago aqui..."
    if request.POST:
        state = "Creado pago"
        formulario = PagosForm(request.POST, user=request.user)
        if formulario.is_valid:
            n = 0
            pago = formulario.save()
            for usuario in request.POST.getlist('usuarios'):
                n = n + 1
                u = Usuarios_Pagos(usuario_id=usuario, pago_id=pago.id)
                u.save()
                if not LOCALHOST:
                    send_mail('ASIGNACION DE PAGO ', "Se le ha asignado el pago\nhttp://prueba1.bueninvento.net/pagos/pagar/" + str(pago.id), 'antoni@bueninvento.es',
                              [User.objects.get(id=usuario).email], fail_silently=False)
            if(n > 0):
                pago.precio = pago.precio / n
                pago.save()
            return HttpResponseRedirect('/')
    else:
        formulario = PagosForm(instance=request.user.usuario, user=request.user)
    return render_to_response('pagos.html', {'state':state, 'formulario': formulario}, context_instance=RequestContext(request))

@login_required
def pagar(request, pago_id):
    # What you want the button to do.
    pago = get_object_or_404(Pagos, pk=pago_id)
    usuario_pago = Usuarios_Pagos.objects.get(usuario_id=request.user.id, pago_id=pago.id)
    usuarios_pago = Usuarios_Pagos.objects.filter(pago_id=pago.id)
    paypal_dict = {
        # "business": settings.PAYPAL_RECEIVER_EMAIL,
        "business": pago.correo,
        "amount": pago.precio,
        "item_name": pago.nombre,
        "invoice": "joinity_test_3" + str(pago.id),
        "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://prueba1.bueninvento.net/pagos/confirmado/",
        "cancel_return": "http://prueba1.bueninvento.net/",
        "custom": usuario_pago.id,
        "currency_code": "EUR",  # currency
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    admin = request.user.id = pago.creador.id
    context = {"form": form.sandbox(), "usuarios":usuarios_pago,
               "pago":pago, "admin": admin, "pagado": usuario_pago.ha_pagado}
    return render_to_response("paypal.html", context)

def mis_pagos(request):
    context={"pagina":"misCompras"}
    return render_to_response("pagos/mis_pagos.html", context)
