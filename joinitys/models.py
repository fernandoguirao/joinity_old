from django.db import models
from django.contrib.auth.models import User
from categorias.models import Subcategorias, Subcategorias_Compras, Subcategorias_Family
from reservas.models import Empresa
#############################################################################
#                    CLASE PADRE JOINITY                                    #
#############################################################################
class Joinitys(models.Model):
    nombre = models.TextField(null=True)
    descripcion = models.TextField(null=True, max_length=400)
    tipo=models.IntegerField(default=0)
    n_min=models.IntegerField(default=0)
    n_max=models.IntegerField(default=0)
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    privacidad=models.IntegerField(default=0)
    usuarios = models.ManyToManyField(User, through='Usuarios_Joinity')
    creador = models.ForeignKey(User, related_name="creador_joinity")
#     family=models.OneToOneRel("Family", related_name="family")
    class Meta:
        db_table = "Joinitys"
    def n_joiners(self):
        return Usuarios_Joinity.objects.filter(joinity=self).count()
    def que_soy(self, user):
        if self.soy_admin(user):
            return "admin"
        elif self.soy_miembro(user):
            return "miembro"
        elif self.soy_invitado(user):
            return "invitado"
        elif self.soy_espera(user):
            return "espera"
        else:
            return "nada"
    def soy_admin(self, user):
        return self.creador==user or self.joinity_usuario.filter(usuario=user, estado='2').count()!=0
    def soy_miembro(self, user):
        return self.joinity_usuario.filter(usuario=user, estado='1').count()!=0
    def soy_invitado(self, user):
        return self.joinity_usuario.filter(usuario=user, estado='0').count()!=0
    def soy_espera(self, user):
        return self.joinity_usuario.filter(usuario=user, estado="-1").count()!=0
    def get_categoria(self):
        if self.tipo==1:
            return self.family.subcategoria.nombre
        elif self.tipo==2:
            return self.compras.subcategoria.categoria.nombre
        elif self.tipo==3:
            return self.aficiones.subcategoria.categoria.nombre
    def get_subcategoria(self):
        if self.tipo==1:
            return ""
        elif self.tipo==2:
            return self.compras.subcategoria.nombre
        elif self.tipo==3:
            return self.aficiones.subcategoria.nombre
    def puntuacion_media(self):
        puntuaciones = Puntuaciones.objects.filter(joinity=self)
        total = 0
        n = 0
        for puntuacion in puntuaciones:
            total = total + puntuacion.puntuacion
            n = n + 1
        
        if(n != 0):
            return total / n
        else:
            return 0
    def get_tipo(self):
        if self.tipo==1:
            return "family"
        elif self.tipo==2:
            return "compras"
        elif self.tipo==3:
            return "aficiones"
    def get_porcentaje(self):
        n=self.n_joiners()
        minimo=self.n_min
        maximo=self.n_max
        if maximo==0:
            maximo=100
        if n<minimo:
            return int((n*100)/minimo)
        elif n<maximo:
            return int((n*100)/maximo)
        else:
            return 100
            
        
# ---------TIPOS DE JOINITY-------------#
class Family(models.Model):
    joinity=models.OneToOneField(Joinitys, related_name="family")
    subcategoria = models.ForeignKey(Subcategorias_Family)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    repeticion=models.IntegerField(default=0)
    reserva=models.ManyToManyField(Empresa, through='Reservas_Empresas')
    class Meta:
        db_table="Family"
class Compras(models.Model):
    joinity=models.OneToOneField(Joinitys, related_name="compras")
    subcategoria=models.ForeignKey(Subcategorias_Compras)
    n_descuento1=models.IntegerField(default=0)
    descuento1=models.IntegerField(default=0)
    n_descuento2=models.IntegerField(default=0)
    descuento2=models.IntegerField(default=0)
    n_descuento3=models.IntegerField(default=0)
    descuento3=models.IntegerField(default=0)
    class Meta:
        db_table="Compras"
class Aficiones(models.Model):
    joinity=models.OneToOneField(Joinitys, related_name="aficiones")
    subcategoria = models.ForeignKey(Subcategorias)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    repeticion=models.IntegerField(default=0)
    nivel=models.IntegerField(default=1)
    requisitos=models.CharField(max_length=100)
    class Meta:
        db_table="Aficiones"
#############################################################################


#############################################################################
#                    RELACIONES                                             #
#############################################################################
class Usuarios_Joinity(models.Model):
    usuario = models.ForeignKey(User, related_name="usuario_joinity")
    joinity = models.ForeignKey(Joinitys, related_name="joinity_usuario")
    estado = models.IntegerField(default=0)
    class Meta:
        db_table = "Usuarios_Joinitys"
    def __unicode__(self):
        return self.usuario.first_name
    

##############################################################################
#                     COMPONENTES                                            #
##############################################################################
   

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
        

class Reservas_Empresas(models.Model):
    family=models.ForeignKey(Family, related_name="family_reserva")
    empresa=models.ForeignKey(Empresa, related_name="empresa_reserva")
    comensales=models.IntegerField(default=0)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    estado=models.IntegerField(default=0)
    class Meta:
        db_table="Reservas_Empresas"

     

class Usuarios_Evento(models.Model):
    usuario = models.ForeignKey(User)
    evento = models.ForeignKey(Eventos, related_name="usuarios_evento")
    estado = models.IntegerField(default=0)
    class Meta:
        db_table = "Usuarios_Eventos"
class Usuarios_Tarea(models.Model):
    usuario = models.ForeignKey(User)
    tarea = models.ForeignKey(Tareas)
    estado = models.IntegerField(default=0)
    class Meta:
        db_table = "Usuarios_Tarea"
class Actualizaciones(models.Model):
    joinity=models.ForeignKey(Joinitys, related_name="actualizaciones")
    tipo=models.IntegerField()
    class Meta:
        db_table="Actualizaciones"
class Texto_Joinity(models.Model):
    usuario=models.ForeignKey(User)
    actualizacion=models.OneToOneField(Actualizaciones, related_name="texto")
    contenido=models.TextField(max_length=400)
    class Meta:
        db_table="Texto_Joinitys"
class Comentario_Actualizacion(models.Model):
    usuario=models.ForeignKey(User)
    actualizacion=models.ForeignKey(Actualizaciones, related_name="comentarios")
    comentario=models.TextField(max_length=400)
    class Meta:
        db_table="Comentarios_Actualizaciones"
class Lugares_Joinity(models.Model):
    joinity=models.ForeignKey(Joinitys, related_name="lugares")
    n=models.IntegerField(default=1)
    lugar=models.TextField()
    class Meta:
        db_table="Lugares_Joinitys"
class Lugares_Evento(models.Model):
    evento=models.ForeignKey(Eventos, related_name="lugares_evento")
    n=models.IntegerField(default=1)
    lugar=models.TextField()
    class Meta:
        db_table="Lugares_Eventos"
class Lugares_Tarea(models.Model):
    tarea=models.ForeignKey(Tareas, related_name="lugares_tarea")
    n=models.IntegerField(default=1)
    lugar=models.TextField()
    class Meta:
        db_table="Lugares_Tareas"
class Foto_Joinity(models.Model):
    usuario=models.ForeignKey(User, related_name="foto_usuario_actualizaciones")
    actualizacion=models.OneToOneField(Actualizaciones, related_name="foto")
    contenido = models.ImageField(max_length=100, upload_to='joinity', blank=True, null=True)
    class Meta:
        db_table="Foto_Joinitys"

class Puntuaciones(models.Model):
    joinity = models.ForeignKey(Joinitys, related_name="puntuacion")
    usuario = models.ForeignKey(User, related_name="puntuador_joinitys")
    puntuacion = models.IntegerField(default=0)
    class Meta:
        db_table = "Puntuaciones_Joinity"

class Joinitys_VIP(models.Model):
    joinity=models.ForeignKey(Joinitys, related_name="joinity_vip")
    class Meta:
        db_table="Joinitys_VIP"