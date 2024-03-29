from django.db import models
from django.contrib.auth.models import User
from joinitys.models import Joinitys

class Eventos(models.Model):
    titulo=models.TextField()
    descripcion=models.TextField(null=True, max_length=400)
    privacidad=models.IntegerField(default=0)
    privilegios=models.IntegerField(default=0)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    repeticion=models.IntegerField(default=0)
    creador=models.ForeignKey(User, related_name="creador_evento")
    joinity=models.ForeignKey(Joinitys, related_name="eventos")
    foto = models.ImageField(max_length=100, upload_to='eventos', blank=True, null=True)
    usuarios=models.ManyToManyField(User, through='Usuarios_Evento')
    class Meta:
        db_table = "Eventos"
    def n_joiners(self):
        return Usuarios_Evento.objects.filter(evento=self).count()
class Usuarios_Evento(models.Model):
    usuario = models.ForeignKey(User)
    evento = models.ForeignKey(Eventos, related_name="usuarios_evento")
    estado = models.IntegerField(default=0)
    class Meta:
        db_table = "Usuarios_Eventos"
class Lugares_Evento(models.Model):
    evento=models.ForeignKey(Eventos, related_name="lugares_evento")
    n=models.IntegerField(default=1)
    lugar=models.TextField()
    class Meta:
        db_table="Lugares_Eventos"
class Actualizaciones_Eventos(models.Model):
    evento=models.ForeignKey(Eventos, related_name="actualizaciones")
    tipo=models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table="Actualizaciones_Eventos"
class Texto_Evento(models.Model):
    usuario=models.ForeignKey(User)
    actualizacion=models.OneToOneField(Actualizaciones_Eventos, related_name="texto")
    contenido=models.TextField(max_length=400)
    class Meta:
        db_table="Texto_Eventos"
class Comentario_Evento(models.Model):
    usuario=models.ForeignKey(User)
    actualizacion=models.ForeignKey(Actualizaciones_Eventos, related_name="comentarios")
    comentario=models.TextField(max_length=400)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table="Comentarios_Actualizaciones_Eventos"