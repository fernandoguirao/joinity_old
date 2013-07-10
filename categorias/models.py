from django.db import models

class Categorias(models.Model):
    nombre = models.CharField(max_length="40")
    class Meta:
        db_table = "Categorias"
    def __unicode__(self):
        return self.nombre
class Subcategorias(models.Model):
    categoria = models.ForeignKey(Categorias, related_name="subcategorias-categorias")
    nombre = models.CharField(max_length="40")
    class Meta:
        db_table = "Subcategorias"
    def __unicode__(self):
        return self.categoria.nombre + "-" + self.nombre
class Categorias_Compras(models.Model):
    nombre = models.CharField(max_length="40")
    class Meta:
        db_table = "Categorias_Compras"
    def __unicode__(self):
        return self.nombre
class Subcategorias_Compras(models.Model):
    categoria = models.ForeignKey(Categorias_Compras, related_name="subcategorias-categorias-compras")
    nombre = models.CharField(max_length="40")
    class Meta:
        db_table = "Subcategorias_Compras"
    def __unicode__(self):
        return self.categoria.nombre + "-" + self.nombre

class Subcategorias_Family(models.Model):
    nombre = models.CharField(max_length="40")
    class Meta:
        db_table = "Subcategorias_Family"
    def __unicode__(self):
        return self.nombre

# Create your models here.
