from django.db import models
from django.contrib.auth.models import User

class Mensajes(models.Model):
    remitente = models.ForeignKey(User, related_name="remitente_mensaje")
    destinatario = models.ForeignKey(User, related_name="destinatario_mensaje")
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    estado = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "Mensajes"
    def leido(self):
        return self.estado == 1
# Create your models here.
