from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.shortcuts import get_object_or_404
from models import Pagos, Usuarios_Pagos
from django.template.loader import render_to_string
from joinity.settings import SITE_NAME
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm

@dajaxice_register
def carga(request, pago_id):
    pago=get_object_or_404(Pagos, pk=pago_id)
    usuario_pago=Usuarios_Pagos.objects.get(usuario=request.user, pago=pago)
    paypal_dict = {
        # "business": settings.PAYPAL_RECEIVER_EMAIL,
        "business": pago.correo,
        "amount": pago.get_precio,
        "item_name": pago.concepto,
        "invoice": "pagos_family_test" + str(pago.id),
        "notify_url": "%s%s" % (SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://prueba1.bueninvento.net/pagos/confirmado/",
        "cancel_return": "http://joinity.com/",
        "custom": usuario_pago.id,
        "currency_code": "EUR",  # currency
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    context={"pago":pago, "form":form.sandbox()}
    pagina_pago=render_to_string("joinitys/pagos/ajax_ver_pago.html", context)
    return simplejson.dumps({"pago":pagina_pago})