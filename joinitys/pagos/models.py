from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from joinity.settings import LOCALHOST
from joinitys.models import Joinitys
from datetime import datetime

# Create your models here.
from paypal.standard.ipn.signals import payment_was_successful

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    usuariopago = Usuarios_Pagos.objects.get(pk=ipn_obj.custom)
    usuariopago.estado = 1
    usuariopago.save()
    pago = Pagos.objects.get(pk=usuariopago.pago_id)
    usuario = User.objects.get(pk=usuariopago.usuario_id)
    if not LOCALHOST:
        send_mail('CONFIRMACION DE PAGO ', 'Se confirma el pago por el producto:', 'joinity@joinity.com',
                  [usuario.email], fail_silently=False)
        send_mail('CONFIRMACION DE PAGO ', "El usuario: " + usuario.email + " ha pagado el producto", 'joinity@joinity.com',
                  [pago.correo], fail_silently=False)
        send_mail('CONFIRMACION DE PAGO ', "El usuario: " + usuario.email + " ha pagado el producto:\nConcepto: "+ pago.concepto
                  +"\nPrecio: "+str(pago.get_precio())+"\nFecha: "+str(datetime.now())+"\nal usuario: "+pago.correo, 'joinity@joinity.com',
                  ["fernando@bueninvento.es"], fail_silently=False)
        if(pago.correo != pago.creador.email):
            send_mail('CONFIRMACION DE PAGO ', "El usuario: " + usuario.email + " ha pagado el producto", 'joinity@joinity.com',
            [pago.creador.email], fail_silently=False)

payment_was_successful.connect(show_me_the_money)

# Create your models here.

class Pagos(models.Model):
    correo = models.TextField(null=True, max_length=100)
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    concepto = models.TextField(null=True)
    producto=models.TextField(null=True)
    descripcion=models.TextField(max_length=400)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    usuarios = models.ManyToManyField(User, through='Usuarios_Pagos')
    creador = models.ForeignKey(User, related_name="creador")
    joinity= models.ForeignKey(Joinitys, related_name="pagos")
    class Meta:
        db_table = "Pagos"
    def get_precio(self):
        n=Usuarios_Pagos.objects.filter(pago=self).count()
        return self.precio/n

class Usuarios_Pagos(models.Model):
    usuario = models.ForeignKey(User)
    pago = models.ForeignKey(Pagos)
    estado = models.IntegerField(default=0)
    class Meta:
        db_table = "Usuarios_Pagos"
    def ha_pagado(self):
        return self.estado == 1
    def get_nombre(self):
        return "patata"
