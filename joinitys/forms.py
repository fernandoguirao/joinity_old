# -*- encoding: utf-8 -*-

from django import forms
from models import Joinitys, Texto_Joinity, Eventos, Lugares_Evento, Lugares_Tarea, Puntuaciones, Actualizaciones
from models import Tareas, Family, Compras, Aficiones, Lugares_Joinity, Foto_Joinity, Reservas_Empresas
from models import Comentario_Actualizacion

class JoinityForm(forms.ModelForm):
    nombre=forms.CharField()
    descripcion = forms.Textarea()
    n_min=forms.IntegerField()
    n_max=forms.IntegerField()
    precio = forms.DecimalField(localize=True)
    #usuarios = forms.CheckboxSelectMultiple()
    privacidad=forms.ChoiceField(choices=([("0", "Publico"), ("1","Peticion de invitacion"), ("2", "Privado")]))
    class Meta:
        model = Joinitys
        fields = ('nombre','descripcion', 'n_min', 'n_max', 'precio', 'privacidad')
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._tipo = kwargs.pop('tipo')
        super(JoinityForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        joinity = super(JoinityForm, self).save(commit=False)
        joinity.creador = self._user
        joinity.tipo=self._tipo
        if commit:
            joinity.save()
            # self.save_m2m()
        return joinity
class FamilyForm(forms.ModelForm):
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)

    class Meta:
        model = Family
        fields=("subcategoria", "fecha_inicio", "fecha_fin", "repeticion")
    def __init__(self, *args, **kwargs):
        self._joinity = kwargs.pop('joinity')
        super(FamilyForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        family = super(FamilyForm, self).save(commit=False)
        family.joinity = self._joinity
        if commit:
            family.save()
        return family
class AficionesForm(forms.ModelForm):
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    nivel = forms.ChoiceField(choices=([("0", "Indiferente"), ("1", "Amateur"), ("2", "Intermedio"), ("3", "Pro")]), required=True)

    class Meta:
        model = Aficiones
        fields=("subcategoria", "fecha_inicio", "fecha_fin", "repeticion", "nivel", "requisitos")
    def __init__(self, *args, **kwargs):
        self._joinity = kwargs.pop('joinity')
        super(AficionesForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        aficion = super(AficionesForm, self).save(commit=False)
        aficion.joinity = self._joinity
        if commit:
            aficion.save()
        return aficion
        # pago.email = self.cleaned_data["email"]
class ComprasForm(forms.ModelForm):
    class Meta:
        model = Compras
        fields=("subcategoria", "n_descuento1", "descuento1", "n_descuento2", "descuento2", "n_descuento3", "descuento3")
    def __init__(self, *args, **kwargs):
        self._joinity = kwargs.pop('joinity')
        super(ComprasForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        compras = super(ComprasForm, self).save(commit=False)
        compras.joinity = self._joinity
        if commit:
            compras.save()
        return compras
        # pago.email = self.cleaned_data["email"]
class FormFoto(forms.ModelForm):
    contenido=forms.ImageField(required=False)
    class Meta:
        model=Foto_Joinity
        fields=("contenido",)
    def __init__(self, *args, **kwargs):
        self._joinity=kwargs.pop('joinity')
        self._usuario=kwargs.pop('usuario')
        super(FormFoto, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        nueva=super(FormFoto, self).save(commit=False)
        actualizacion=Actualizaciones(joinity=self._joinity, tipo=2)
        actualizacion.save()
        nueva.actualizacion=actualizacion
        nueva.usuario=self._usuario
        if commit:
            nueva.save()
        return nueva

class FormTexto(forms.ModelForm):
    contenido = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cuéntale algo al grupo.', 'id':'appendedInputButton-02', 'class':'span2'}))
    class Meta:
        model = Texto_Joinity
        fields = ("contenido",)

    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._joinity = kwargs.pop('joinity')
        super(FormTexto, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nuevo_texto = super(FormTexto, self).save(commit=False)
        actualizacion=Actualizaciones(joinity=self._joinity, tipo=1)
        actualizacion.save()
        nuevo_texto.usuario = self._usuario
        nuevo_texto.actualizacion = actualizacion
        if commit:
            nuevo_texto.save()
            # self.save_m2m()
        return nuevo_texto
class FormComentario(forms.ModelForm):
    comentario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cuéntale algo al grupo.', 'class':'span2 inputNormal'}))
    class Meta:
        model = Comentario_Actualizacion
        fields = ("comentario",)

    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._actualizacion = kwargs.pop('actualizacion')
        super(FormComentario, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nuevo_comentario = super(FormComentario, self).save(commit=False)
        nuevo_comentario.usuario = self._usuario
        nuevo_comentario.actualizacion = self._actualizacion
        if commit:
            nuevo_comentario.save()
            # self.save_m2m()
        return nuevo_comentario
class Crear_Evento(forms.ModelForm):
    titulo=forms.CharField()
    foto = forms.ImageField(required=False)
    privacidad=forms.ChoiceField(choices=([("0", "Publico"), ("1", "Privado")]))
    privilegios=forms.ChoiceField(choices=([("0", "Solo administrador"), ("1", "Todos los participantes")]))
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    class Meta:
        model=Eventos
        fields=("titulo", "descripcion", "fecha_inicio", "fecha_fin", "foto", "privacidad", "privilegios","repeticion", )
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._joinity=kwargs.pop('joinity')
        super(Crear_Evento, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        evento = super(Crear_Evento, self).save(commit=False)
        evento.creador = self._user
        evento.joinity=self._joinity
        if commit:
            evento.save()
            # self.save_m2m()
        return evento

class Crear_Tarea(forms.ModelForm):
    nombre=forms.CharField()
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    foto = forms.ImageField(required=False)
    class Meta:
        model=Tareas
        fields=("nombre", "notas", "fecha_inicio", "fecha_fin", "repeticion", "foto" )
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._joinity=kwargs.pop('joinity')
        super(Crear_Tarea, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        tarea = super(Crear_Tarea, self).save(commit=False)
        tarea.creador = self._user
        tarea.joinity=self._joinity
        if commit:
            tarea.save()
        return tarea
class Anyadir_Lugar(forms.Form):
    lugar=forms.CharField()
    class Meta:
        model=Lugares_Joinity
        fields=("lugar")
class Anyadir_Lugar_Evento(forms.Form):
    lugar=forms.CharField()
    class Meta:
        model=Lugares_Evento
        fields=("lugar")
class Anyadir_Lugar_Tarea(forms.Form):
    lugar=forms.CharField()
    class Meta:
        model=Lugares_Tarea
        fields=("lugar")
class Buscar(forms.Form):
    s = forms.CharField()
class Reservar(forms.ModelForm):
    class Meta:
        model=Reservas_Empresas
        fields=("comensales", "fecha_inicio", "fecha_fin")
    def __init__(self, *args, **kwargs):
        self._family = kwargs.pop('family')
        self._empresa=kwargs.pop('empresa')
        super(Reservar, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        reserva = super(Reservar, self).save(commit=False)
        reserva.family = self._family
        reserva.empresa=self._empresa
        if commit:
            reserva.save()
        return reserva
class Puntuar(forms.ModelForm):
    puntuacion = forms.ChoiceField(choices=([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]), required=True)

    class Meta:
        model = Puntuaciones
        fields = ("puntuacion",)

    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._joinity = kwargs.pop('joinity')
        super(Puntuar, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nueva_puntuacion = super(Puntuar, self).save(commit=False)
        nueva_puntuacion.joinity = self._joinity
        nueva_puntuacion.usuario = self._usuario
        if commit:
            nueva_puntuacion.save()
            # self.save_m2m()
        return nueva_puntuacion
