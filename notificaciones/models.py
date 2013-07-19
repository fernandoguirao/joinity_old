from django.db import models
from django.contrib.auth.models import User
from mensajes.models import Mensajes
from joinitys.models import Joinitys
from joinitys.eventos.models import Eventos
from joinitys.tareas.models import Tareas
# Create your models here.
class Notificaciones:
    usuario=models.ForeignKey(User, related_name="notificaciones")
    tipo=models.IntegerField(default=0)
    estado=models.IntegerField(default=0)
    id_notificacion=models.IntegerField(default=0)
    class Meta:
        db_table = "Notificaciones"
    def notificacion(self):
        if self.tipo==0: #mensajes
            return Mensajes.objects.get(pk=self.id_notificacion)
        elif self.tipo==1: #invitacion joinity
            return Joinitys.objects.get(pk=self.id_notificacion)
        elif self.tipo==2: #invitacion eventos
            return Eventos.objects.get(pk=self.id_notificacion)
        elif self.tipo==3:#invitacion tareas
            return Tareas.objects.get(pk=self.id_notificacion)
        return False

            
