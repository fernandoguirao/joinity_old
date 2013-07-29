# -*- encoding: utf-8 -*-

from django import forms
from models import Texto_Joinity, Puntuaciones, Actualizaciones
from models import Foto_Joinity, Reserva_Brand, Votacion
from models import Comentario_Actualizacion
        # pago.email = self.cleaned_data["email"]
class FormFoto(forms.ModelForm):
    contenido=forms.ImageField(widget=forms.ClearableFileInput(attrs={'id':'appendedInputButton-02', 'class':'span2 hayfoto btn'}))
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
        texto=nuevo_texto.contenido
        youtube=texto.find("youtube.com/watch?v=")
        cadena=""
        tipo=1
        if youtube>=0:
            for letra in texto[youtube:]:
                if letra==" ":
                    break
                else:
                    cadena=cadena+letra
            nuevo_texto.contenido=cadena
            tipo=3
        
        actualizacion=Actualizaciones(joinity=self._joinity, tipo=tipo)
        actualizacion.save()
        nuevo_texto.usuario = self._usuario
        nuevo_texto.actualizacion = actualizacion
        if commit:
            nuevo_texto.save()
            
        return nuevo_texto
class FormComentario(forms.ModelForm):
    comentario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cuéntale algo al grupo.', 'class':'span2 inputNormal inputcomentario'}))
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
class FormVotacion(forms.ModelForm):
    pregunta = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cuál sería el título de la pregunta', 'id':'pregunta_votacion', 'class':'inputNormal input-small titulopregunta'}))
    class Meta:
        model = Votacion
        fields = ("pregunta",)

    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._joinity = kwargs.pop('joinity')
        super(FormVotacion, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nueva_votacion = super(FormVotacion, self).save(commit=False)
        tipo=4
        actualizacion=Actualizaciones(joinity=self._joinity, tipo=tipo)
        actualizacion.save()
        nueva_votacion.usuario = self._usuario
        nueva_votacion.actualizacion = actualizacion
        if commit:
            nueva_votacion.save()  
        return nueva_votacion

class Buscar(forms.Form):
    s = forms.CharField()
class Reservar(forms.ModelForm):
    class Meta:
        model=Reserva_Brand
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
