from django import template
register = template.Library()
from joinitys.pagos.models import Usuarios_Pagos

@register.filter(name='ha_pagado')
def ha_pagado(value, arg):
    usuario_pago=Usuarios_Pagos.objects.get(usuario=arg, pago=value)
    return usuario_pago.estado==1
