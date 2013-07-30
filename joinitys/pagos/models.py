from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from joinity.settings import LOCALHOST
from joinitys.models import Joinitys, Usuarios_Joinity
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
    def get_descuento(self):
        if (self.joinity.tipo!=2):
            return 0
        else:
            n=Usuarios_Joinity.objects.filter(joinity=self.joinity).count()
            if self.joinity.compras.n_descuento3<=n:
                descuento=self.joinity.compras.descuento3
            elif self.joinity.compras.n_descuento2<=n:
                descuento=self.joinity.compras.descuento2
            elif self.joinity.compras.n_descuento1<=n:
                descuento=self.joinity.compras.descuento1
            else:
                descuento=0
            return descuento
    def get_precio(self):
        if (self.joinity.tipo!=2):
            n=Usuarios_Pagos.objects.filter(pago=self).count()
            return self.precio/n
        else:
            return self.joinity.precio-(self.joinity.precio*self.get_descuento()/100)
    def get_iva(self):
        precio=self.get_precio()
        return precio*self.joinity.compras.iva/100
    def get_subtotal(self):
        return self.get_precio()+self.joinity.compras.envio
    def get_precio_total(self):
        if (self.joinity.tipo!=2):
            return self.get_precio()
        else:
            return self.get_precio()+self.get_iva()+self.joinity.compras.envio
    def ya_paso(self):
        if (self.joinity.tipo!=2):
            return True
        else:
            fecha_fin=self.joinity.compras.fecha_fin
            
            if fecha_fin.year>datetime.now().year:
                return False
            elif fecha_fin.year==datetime.now().year:
                if fecha_fin.month>datetime.now().month:
                    return False
                elif fecha_fin.month==datetime.now().month:
                    if fecha_fin.day>datetime.now().day:
                        return False
                    elif fecha_fin.day==datetime.now().day:
                        if fecha_fin.hour>datetime.now().hour:
                            return False
                        elif fecha_fin.hour==datetime.now().hour:
                            if fecha_fin.minute>datetime.now().minute:
                                return False
                            else:
                                return True
                        else:
                            return True
                        return True
                    else:
                        return True
                else:  
                    return True
            else:
                return True
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
