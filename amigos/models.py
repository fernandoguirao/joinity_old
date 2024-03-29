from django.db import models
from django.contrib.auth.models import User

class Amigos(models.Model):
    usuario = models.ForeignKey(User, related_name="usuario_amigos")
    amigo = models.ForeignKey(User, related_name="amigo")
    estado = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "Amigos"
# Create your models here.
