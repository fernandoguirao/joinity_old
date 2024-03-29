from django.db import models
from django.contrib.auth.models import User
from categorias.models import Subcategorias, Subcategorias_Compras
from amigos.models import Amigos
from mensajes.models import Mensajes
from joinitys.models import Usuarios_Joinity, Actualizaciones, Comentario_Actualizacion
from notificaciones.models import Notificaciones
from brands.models import Brand
class Puntuaciones(models.Model):
    usuario = models.ForeignKey(User, related_name="usuario_puntuado")
    puntuador = models.ForeignKey(User, related_name="usuario_puntuador")
    puntuacion = models.IntegerField(default=0)
    class Meta:
        db_table = "Puntuaciones"
# Create your models here.

class Usuarios(models.Model):
    usuario = models.OneToOneField(User, unique=True, related_name='usuario', primary_key=True)
    foto = models.ImageField(max_length=100, upload_to='avatars', blank=True, null=True, default="defaults/avatar.jpeg")
    nacimiento = models.DateField(null=True)
    sexo = models.IntegerField(null=True)
    ciudad = models.TextField(null=True, max_length=50, verbose_name='ciudad')
    cpostal = models.IntegerField(null=True)
    dni = models.TextField(null=True, max_length=14)
    telefono = models.IntegerField(null=True, max_length=15)
    universidad = models.TextField(null=True, max_length=100)
    empresa = models.TextField(null=True, max_length=100)
    intereses_comprar = models.ManyToManyField(Subcategorias_Compras, blank=True, null=True)
    intereses = models.ManyToManyField(Subcategorias, blank=True, null=True)
    visible = models.IntegerField(default=1)
    avisar = models.IntegerField(default=1)
    ubicacion_visible = models.IntegerField(default=1)
    ocultar_perfil = models.IntegerField(default=1)
    blogger=models.BooleanField(default=0)
    blog=models.TextField(null=True)
    intereses_blog=models.ManyToManyField(Subcategorias, blank=True, null=True, related_name='intereses_blog')
    # activation_key=models.CharField(max_length=40)
    # key_expires = models.DateTimeField()

    class Meta:
        db_table = "Usuarios"
        verbose_name_plural = "usuarios"

    def soy_brand(self):
        return Brand.objects.filter(admin=self).exists()
    def es_hombre(self):
        return self.sexo == 0;
    def son_amigos(self, user_id):
        amigos = Amigos.objects.filter(usuario=user_id, amigo=self.usuario, estado=1).count()
        return amigos != 0
    def solicitud_amistad(self, user_id):
        amigos = Amigos.objects.filter(usuario=user_id, amigo=self.usuario, estado=0)
        return amigos.count() != 0
    def solicitudes(self):
        n_solicitudes = Amigos.objects.filter(amigo=self.usuario, estado=0).count()
        return n_solicitudes
    def oculto(self):
        return self.ocultar_perfil == 1;
    def mensajes(self):
        n_mensajes = Mensajes.objects.filter(destinatario=self.usuario, estado=0).count()
        return n_mensajes;
    def su_ciudad(self, c):
        if self.ciudad == c:
            return self
        return False
    def invitado_joinity(self, joinity):
        usuarios_joinity=Usuarios_Joinity.objects.filter(usuario=self.usuario, joinity=joinity).count()
        return usuarios_joinity != 0
    def puntuacion_media(self):
        puntuaciones = Puntuaciones.objects.filter(usuario=self.usuario)
        total = 0
        n = 0
        for puntuacion in puntuaciones:
            total = total + puntuacion.puntuacion
            n = n + 1
        
        if(n != 0):
            return total / n
        else:
            return 0
    def tiene_notificaciones(self):
        return Notificaciones.objects.filter(usuario=self, estado=0).exists()
    def n_notificaciones(self):
        return Notificaciones.objects.filter(usuario=self, estado=0).count()
    def get_notificaciones(self):
        return Notificaciones.objects.filter(usuario=self).order_by("estado", "-fecha")[:7]
    def get_tiene_mensajes_nuevos(self):
        return Notificaciones.objects.filter(usuario=self, estado=0, tipo=0).exists()
    def get_tiene_joinitys_nuevos(self):
        return Notificaciones.objects.filter(usuario=self, estado=0, tipo=1).exists()
    def get_tiene_eventos_nuevos(self):
        return Notificaciones.objects.filter(usuario=self, estado=0, tipo=2).exists()
    def get_tiene_tareas_nuevas(self):
        return Notificaciones.objects.filter(usuario=self, estado=0, tipo=3).exists()
    def get_tiene_pagos_nuevos(self):
        return Notificaciones.objects.filter(usuario=self, estado=0, tipo=4).exists()
    def get_tiene_reservas_nuevas(self):
        return Notificaciones.objects.filter(usuario=self, estado=0, tipo=5).exists()
    def get_ultimos_joinitys(self):
        joinitys=[]
        lista=[]
        actualizaciones=Actualizaciones.objects.filter(tipo=1, texto__usuario_id=self.usuario.id).order_by("-fecha")[:8]
        for actualizacion in actualizaciones:
            if actualizacion.joinity not in joinitys:
                joinitys.append(actualizacion.joinity)
                nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                lista.append(nuevo)
            else:
                for elemento in lista:
                    if elemento["joinity"]==actualizacion.joinity:
                        if elemento["fecha"]<actualizacion.fecha:
                            elemento["fecha"]=actualizacion.fecha
            comentarios=Comentario_Actualizacion.objects.filter(usuario=self.usuario, actualizacion=actualizacion)
            for comentario in comentarios:
                if comentario.actualizacion.joinity not in joinitys:
                    joinitys.append(actualizacion.joinity)
                    nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                    lista.append(nuevo)
                else:
                    for elemento in lista:
                        if elemento["joinity"]==comentario.actualizacion.joinity:
                            if elemento["fecha"]<actualizacion.fecha:
                                elemento["fecha"]=actualizacion.fecha
                
        actualizaciones=Actualizaciones.objects.filter(tipo=2, foto__usuario_id=self.usuario.id).order_by("-fecha")[:8]
        for actualizacion in actualizaciones:
            if actualizacion.joinity not in joinitys:
                joinitys.append(actualizacion.joinity)
                nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                lista.append(nuevo)
            else:
                for elemento in lista:
                    if elemento["joinity"]==actualizacion.joinity:
                        if elemento["fecha"]<actualizacion.fecha:
                            elemento["fecha"]=actualizacion.fecha
            comentarios=Comentario_Actualizacion.objects.filter(usuario=self.usuario, actualizacion=actualizacion)
            for comentario in comentarios:
                if comentario.actualizacion.joinity not in joinitys:
                    joinitys.append(actualizacion.joinity)
                    nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                    lista.append(nuevo)
                else:
                    for elemento in lista:
                        if elemento["joinity"]==comentario.actualizacion.joinity:
                            if elemento["fecha"]<actualizacion.fecha:
                                elemento["fecha"]=actualizacion.fecha
        actualizaciones=Actualizaciones.objects.filter(tipo=3, texto__usuario_id=self.usuario.id).order_by("-fecha")[:8]
        for actualizacion in actualizaciones:
            if actualizacion.joinity not in joinitys:
                joinitys.append(actualizacion.joinity)
                nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                lista.append(nuevo)
            else:
                for elemento in lista:
                    if elemento["joinity"]==actualizacion.joinity:
                        if elemento["fecha"]<actualizacion.fecha:
                            elemento["fecha"]=actualizacion.fecha
            comentarios=Comentario_Actualizacion.objects.filter(usuario=self.usuario, actualizacion=actualizacion)
            for comentario in comentarios:
                if comentario.actualizacion.joinity not in joinitys:
                    joinitys.append(actualizacion.joinity)
                    nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                    lista.append(nuevo)
                else:
                    for elemento in lista:
                        if elemento["joinity"]==comentario.actualizacion.joinity:
                            if elemento["fecha"]<actualizacion.fecha:
                                elemento["fecha"]=actualizacion.fecha
        actualizaciones=Actualizaciones.objects.filter(tipo=4, votacion__usuario_id=self.usuario.id).order_by("-fecha")[:8]
        for actualizacion in actualizaciones:
            if actualizacion.joinity not in joinitys:
                joinitys.append(actualizacion.joinity)
                nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                lista.append(nuevo)
            else:
                for elemento in lista:
                    if elemento["joinity"]==actualizacion.joinity:
                        if elemento["fecha"]<actualizacion.fecha:
                            elemento["fecha"]=actualizacion.fecha
            comentarios=Comentario_Actualizacion.objects.filter(usuario=self.usuario, actualizacion=actualizacion)
            for comentario in comentarios:
                if comentario.actualizacion.joinity not in joinitys:
                    joinitys.append(actualizacion.joinity)
                    nuevo={"joinity": actualizacion.joinity, "fecha": actualizacion.fecha}
                    lista.append(nuevo)
                else:
                    for elemento in lista:
                        if elemento["joinity"]==comentario.actualizacion.joinity:
                            if elemento["fecha"]<actualizacion.fecha:
                                elemento["fecha"]=actualizacion.fecha
        
        lista.sort(key=lambda tup: tup["fecha"], reverse=True)
        joinitys=[]
        for elemento in lista[:8]:
            joinitys.append(elemento["joinity"])
        return joinitys
            
                
        