from django.db import models
from django.contrib.auth.models import User
from joinitys.models import Joinitys

class Tareas(models.Model):
    nombre=models.TextField()
    notas=models.TextField(null=True, max_length=400)
    foto = models.ImageField(max_length=100, upload_to='tareas', blank=True, null=True)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    repeticion=models.IntegerField(default=0)
    creador=models.ForeignKey(User, related_name="creador_tarea")
    joinity=models.ForeignKey(Joinitys, related_name="tareas")
    usuarios=models.ManyToManyField(User, through='Usuarios_Tarea')
    padre=models.ForeignKey('Tareas', related_name="hijas", null=True)
    class Meta:
        db_table = "Tareas"
class Usuarios_Tarea(models.Model):
    usuario = models.ForeignKey(User)
    tarea = models.ForeignKey(Tareas, related_name="usuarios_tarea")
    estado = models.IntegerField(default=0)
    completada = models.BooleanField(default=False)
    class Meta:
        db_table = "Usuarios_Tarea"
class Lugares_Tarea(models.Model):
    tarea=models.ForeignKey(Tareas, related_name="lugares_tarea")
    n=models.IntegerField(default=1)
    lugar=models.TextField()
    class Meta:
        db_table="Lugares_Tareas"