from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    nombre=models.TextField()
    web=models.TextField()
    tipo=models.TextField(null=True, max_length=100)
    calificacion=models.IntegerField(default=0)
    admin=models.ForeignKey(User, related_name="brand_admin")
    clase=models.IntegerField(default=0)
    imagen_cabecera=models.ImageField(max_length=100, upload_to='brands', blank=True, null=True, default="defaults/avatar.jpeg")
    video=models.TextField(blank=True, null=True)
    imagen_fondo=models.ImageField(max_length=100, upload_to='brands', blank=True, null=True, default="defaults/avatar.jpeg")
    seguidores=models.ManyToManyField(User)
    
    class Meta:
        db_table = "Brands"
    def __unicode__(self):
        return self.nombre
    def puntuacion_media(self):
        puntuaciones = Puntuaciones.objects.filter(empresa=self)
        total = 0
        n = 0
        for puntuacion in puntuaciones:
            total = total + puntuacion.puntuacion
            n = n + 1
        
        if(n != 0):
            return total / n
        else:
            return 0
    def get_reservas(self):
        return self.reservas.exclude(estado=0)
        
# Create your models here.

class Comentarios(models.Model):
    empresa=models.ForeignKey(Brand, related_name="comentarios")
    usuario=models.ForeignKey(User, related_name="comenta_brand")
    comentario=models.CharField(max_length=500)
    class Meta:
        db_table="Comentarios_Brands"
class Fotos(models.Model):
    empresa=models.ForeignKey(Brand, related_name="fotos")
    foto = models.ImageField(max_length=100, upload_to='empresas', blank=True, null=True)
    class Meta:
        db_table = "Fotos_Brands"
class Puntuaciones(models.Model):
    empresa = models.ForeignKey(Brand, related_name="puntuacion")
    usuario = models.ForeignKey(User, related_name="puntuador_brand")
    puntuacion = models.IntegerField(default=0)
    class Meta:
        db_table = "Puntuaciones_Brands"

class Ubicaciones(models.Model):
    brand=models.ForeignKey(Brand, related_name="ubicaciones")
    direccion=models.TextField()
    telefono=models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table= "Ubicaciones_Brands"