from django.db import models
from django.contrib.auth.models import User
from categorias.models import Subcategorias, Subcategorias_Compras, Subcategorias_Family
from brands.models import Brand
from datetime import date, datetime
#############################################################################
#                    CLASE PADRE JOINITY                                    #
#############################################################################
class Joinitys(models.Model):
    nombre = models.TextField(null=True)
    descripcion = models.TextField(null=True, max_length=400)
    tipo=models.IntegerField(default=0)
    foto = models.ImageField(max_length=100, upload_to='joinity', blank=True, null=True, default="defaults/avatar.jpeg")
    n_min=models.IntegerField(default=0)
    n_max=models.IntegerField(default=0)
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    privacidad=models.IntegerField(default=0)
    usuarios = models.ManyToManyField(User, through='Usuarios_Joinity')
    creador = models.ForeignKey(User, related_name="creador_joinity")
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)

#     family=models.OneToOneRel("Family", related_name="family")
    class Meta:
        db_table = "Joinitys"
    def get_multimedia(self):
        multimedia=Actualizaciones.objects.filter(tipo__in=[2,3], joinity_id=self.id)[:3]
        print multimedia
        return multimedia
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
        return self.creador==user or self.joinity_usuario.filter(usuario=user, estado='2').exists()
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
    def sub(self):
        if self.tipo==1:
            return self.family
        elif self.tipo==2:
            return self.compras
        elif self.tipo==3:
            return self.aficiones
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
    def empezo(self):
        if self.get_tipo()!="compras":
            return self.sub().fecha_inicio<=date.today()
    def hasta(self):
        if self.empezo():
            return self.hasta_fin()
        else:
            return self.hasta_inicio()
    def hasta_inicio(self):
        if self.get_tipo()!="compras":
            return (self.sub().fecha_inicio-date.today()).days
        return False
    def hasta_fin(self):
        if self.get_tipo()!="compras":
            return (self.sub().fecha_fin-date.today()).days
        return False
    def lugar(self):
        try:
            return self.lugares.all()[0].get_ciudad()
        except:
            return False
        
# ---------TIPOS DE JOINITY-------------#
class Family(models.Model):
    joinity=models.OneToOneField(Joinitys, related_name="family")
    subcategoria = models.ForeignKey(Subcategorias_Family)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    repeticion=models.IntegerField(default=0)
    reserva=models.ManyToManyField(Brand, through='Reserva_Brand')
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
    envio=models.IntegerField(default=0)
    fecha_fin=models.DateTimeField(null=True)
    iva=models.IntegerField(default=0)
    brand=models.ForeignKey(Brand, related_name="joinitys")
    class Meta:
        db_table="Compras"
    def get_similares(self):
        return Joinitys.objects.filter(tipo=2, compras__subcategoria=self.subcategoria).exclude(compras=self)
    def get_precio(self):
        try:
            return self.joinity.pagos.all()[0].get_precio()
        except:
            return 0
    def get_descuento(self):
        try:
            return self.joinity.pagos.all()[0].get_descuento()
        except:
            return 0
    def ya_paso(self):
        fecha_fin=self.fecha_fin
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
    def get_nivel(self):
        if self.nivel==0:
            return "Indiferente"
        elif self.nivel==1:
            return "Amateur"
        elif self.nivel==2:
            return "Intermedio"
        elif self.nivel==3:
            return "Pro"
    def get_repeticion(self):
        if self.repeticion==0:
            return "Puntual"
        elif self.repeticion==1:
            return "Diario"
        elif self.repeticion==2:
            return "Semanal"
        elif self.repeticion==3:
            return "2 semanas"
        elif self.repeticion==4:
            return "Mensual"
        elif self.repeticion==5:
            return "Anual"
    def get_similares(self):
        return Joinitys.objects.filter(tipo=3, aficiones__subcategoria=self.subcategoria).exclude(aficiones=self)
#############################################################################


#############################################################################
#                    RELACIONES                                             #
#############################################################################
class Usuarios_Joinity(models.Model):
    usuario = models.ForeignKey(User, related_name="usuario_joinity")
    joinity = models.ForeignKey(Joinitys, related_name="joinity_usuario")
    estado = models.IntegerField(default=0)
    fecha_miembro = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "Usuarios_Joinitys"
    def __unicode__(self):
        return self.usuario.first_name
    
    

##############################################################################
#                     COMPONENTES                                            #
##############################################################################
   




        

class Reserva_Brand(models.Model):
    family=models.ForeignKey(Family, related_name="family_reserva")
    brand=models.ForeignKey(Brand, related_name="brand_reserva")
    comensales=models.IntegerField(default=0)
    fecha_inicio=models.DateField(null=True)
    fecha_fin=models.DateField(null=True)
    estado=models.IntegerField(default=0)
    class Meta:
        db_table="Reservas_Brand"


class Actualizaciones(models.Model):
    joinity=models.ForeignKey(Joinitys, related_name="actualizaciones")
    tipo=models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table="Actualizaciones"
    def get_contenido(self):
        if self.tipo==1:
            return self.texto
        elif self.tipo==2:
            return self.foto
        elif self.tipo==3:
            return self.texto
        elif self.tipo==4:
            return Votacion.objects.get(actualizacion=self)
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
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table="Comentarios_Actualizaciones"
class Votacion(models.Model):
    actualizacion=models.ForeignKey(Actualizaciones, related_name="votacion")
    usuario=models.ForeignKey(User, related_name="creador_votaciones")
    pregunta=models.TextField(max_length=400, blank=True, null=True)
    class Meta:
        db_table="Votaciones"
    def n_votos(self):
        n=0
        for respuesta in self.respuestas.all():
            n+=respuesta.n_votos()
        return n
class Respuesta(models.Model):
    votacion=models.ForeignKey(Votacion, related_name="respuestas")
    respuesta=models.TextField(max_length=400)
    votos=models.ManyToManyField(User)
    class Meta:
        db_table="Respuestas"
    def n_votos(self):
        return self.votos.count()
    def porcentaje(self):
        
        n_votos_total=self.votacion.n_votos()
        if n_votos_total==0:
            return 0
        return self.n_votos()*100/n_votos_total
    
class Lugares_Joinity(models.Model):
    joinity=models.ForeignKey(Joinitys, related_name="lugares")
    n=models.IntegerField(default=1)
    lugar=models.TextField()
    class Meta:
        db_table="Lugares_Joinitys"
    def get_ciudad(self):
        ciudad=""
        for letra in self.lugar:
            if letra!=",":
                ciudad+=letra
            else:
                break
        return ciudad

class Reservas_Joinity(models.Model):
    joinity=models.ForeignKey(Joinitys, related_name="reservas")
    brand=models.ForeignKey(Brand, related_name="reservas")
    usuario=models.ForeignKey(User, related_name="reservas")
    fecha_inicio=models.DateTimeField(null=True, blank=True)
    fecha_fin=models.DateTimeField(null=True, blank=True)
    notas=models.TextField(null=True)
    n_personas=models.IntegerField(default=0)
    n_habitaciones=models.IntegerField(default=0)
    estado=models.IntegerField(default=0)
    class Meta:
        db_table="Reservas_Joinity"

class Foto_Joinity(models.Model):
    usuario=models.ForeignKey(User, related_name="foto_usuario_actualizaciones")
    actualizacion=models.OneToOneField(Actualizaciones, related_name="foto")
    contenido = models.ImageField(max_length=100, upload_to='joinity/actualizacion', blank=True, null=True)
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