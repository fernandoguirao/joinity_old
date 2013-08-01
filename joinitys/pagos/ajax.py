from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.shortcuts import get_object_or_404
from models import Pagos, Usuarios_Pagos
from django.template.loader import render_to_string
from joinity.settings import SITE_NAME, LOCALHOST
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
from forms import PagosForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from joinitys.models import Joinitys
@dajaxice_register
def carga(request, pago_id):
    pago=get_object_or_404(Pagos, pk=pago_id)
    usuario_pago=Usuarios_Pagos.objects.get(usuario=request.user, pago=pago)
    paypal_dict = {
        # "business": settings.PAYPAL_RECEIVER_EMAIL,
        "business": pago.correo,
        "amount": pago.get_precio,
        "item_name": pago.concepto,
        "invoice": "pagos_family" + str(pago.id)+"_"+str(request.user.id),
        "notify_url": "%s%s" % (SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://joinity.com/",
        "cancel_return": "http://joinity.com/",
        "custom": usuario_pago.id,
        "currency_code": "EUR",  # currency
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context={"pago":pago, "form":form.render()}
    pagina_pago=render_to_string("joinitys/pagos/ajax_ver_pago.html", context)
    return simplejson.dumps({"pago":pagina_pago})
@dajaxice_register
def carga_compra(request, pago_id):
    pago=get_object_or_404(Pagos, pk=pago_id)
    usuario_pago=Usuarios_Pagos.objects.get_or_create(usuario=request.user, pago=pago)
    paypal_dict = {
        # "business": settings.PAYPAL_RECEIVER_EMAIL,
        "business": pago.correo,
        "amount": pago.get_precio,
        "item_name": pago.concepto,
        "invoice": "pagos_compras_" + str(pago.id)+"_"+str(request.user.id),
        "notify_url": "%s%s" % (SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://joinity.com/",
        "cancel_return": "http://joinity.com/",
        "custom": usuario_pago[0].id,
        "currency_code": "EUR",  # currency
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    context={"pago":pago, "form":form.render()}
    pagina_pago=render_to_string("joinitys/pagos/ajax_ver_compra.html", context)
    return simplejson.dumps({"pago":pagina_pago})

@dajaxice_register
def crear(request, formulario , joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    form=PagosForm(formulario, joinity=joinity, user=request.user)
    if form.is_valid():
        pago = form.save()
        for usuario in formulario['usuarios']:
            u = Usuarios_Pagos(usuario_id=usuario, pago_id=pago.id)
            u.save()
            if not LOCALHOST:
                send_mail('ASIGNACION DE PAGO ', "Se le ha asignado el pago con el concepto " + str(pago.concepto), 'joinity@joinity.com',
                          [User.objects.get(id=usuario).email], fail_silently=False)
        return simplejson.dumps({"ok":True})
    else:
        return simplejson.dumps({"ok":False})
    