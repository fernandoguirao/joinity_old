from django import template
from datetime import date
from mensajes.models import Mensajes
register = template.Library()

@register.filter(name='es_hoy')
def es_hoy(value):
    delta = value.date() - date.today()
    if delta.days == 0:
        return True
    else:
        return False
@register.filter(name='get_ultimo')
def get_ultimo(value, arg):
    consulta="SELECT * FROM Mensajes "
    consulta=consulta+"WHERE (remitente_id="+str(value.id)+" AND destinatario_id="+str(arg.id)+") "
    consulta=consulta+"OR (remitente_id="+str(arg.id)+" AND destinatario_id="+str(value.id)+") "
    consulta=consulta+"ORDER BY fecha DESC"
    mensaje=Mensajes.objects.raw(consulta)[0]
    return mensaje


@register.filter(name='get_mensaje')
def get_mensaje(value):
    return value.mensaje

@register.filter(name='get_fecha')
def get_fecha(value):
    return value.fecha

@register.filter(name="n_nuevos")
def n_nuevos(value, arg):
    n=Mensajes.objects.filter(destinatario_id=value, remitente_id=arg, estado=0).count()
    n=n+Mensajes.objects.filter(destinatario_id=arg, remitente_id=value, estado=0).count()
    return n

@register.filter(name='leido')
def get_leido(value, arg):
    if value.estado==0 and value.destinatario == arg:
        return True
    else:
        return False