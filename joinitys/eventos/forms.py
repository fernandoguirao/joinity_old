# -*- encoding: utf-8 -*-

from django import forms
from models import Eventos, Lugares_Evento, Texto_Evento, Actualizaciones_Eventos, Comentario_Evento
from datetime import date
class Crear_Evento(forms.ModelForm):
    titulo=forms.CharField(widget=forms.Textarea(attrs={"class":"inputNormal input-small","placeholder":"Ejemplo: 'Fiesta de graduacion de la promocion 2013-2014'"}))
    foto = forms.ImageField(required=False,widget=forms.FileInput({"class":"inputFoto","id":"fotoinput"}))
    privacidad=forms.ChoiceField(choices=([("0", "Publico"), ("1", "Privado")]))
    privilegios=forms.ChoiceField(choices=([("0", "Solo administrador"), ("1", "Todos los participantes")]))
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    fecha_inicio=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-01', 'value':str(date.today())}))
    fecha_fin=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-02', 'value':str(date.today())}))

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
class Anyadir_Lugar(forms.Form):
    lugar=forms.CharField()
    class Meta:
        model=Lugares_Evento
        fields=("lugar")
class FormTexto(forms.ModelForm):
    contenido = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cuéntale algo al grupo.', 'id':'appendedInputButton-02', 'class':'span2'}))
    class Meta:
        model = Texto_Evento
        fields = ("contenido",)

    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._evento = kwargs.pop('evento')
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
        
        actualizacion=Actualizaciones_Eventos(evento=self._evento, tipo=tipo)
        actualizacion.save()
        nuevo_texto.usuario = self._usuario
        nuevo_texto.actualizacion = actualizacion
        if commit:
            nuevo_texto.save()
            
        return nuevo_texto
    
class FormComentario(forms.ModelForm):
    comentario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cuéntale algo al grupo.', 'class':'span2 inputNormal inputcomentario'}))
    class Meta:
        model = Comentario_Evento
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