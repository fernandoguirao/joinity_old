from django import forms
from models import Tareas, Lugares_Tarea

class Crear(forms.ModelForm):
    nombre=forms.CharField()
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    foto = forms.ImageField(required=False)
    class Meta:
        model=Tareas
        fields=("nombre", "notas", "fecha_inicio", "fecha_fin", "repeticion", "foto" )
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._joinity=kwargs.pop('joinity')
        super(Crear, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        tarea = super(Crear, self).save(commit=False)
        tarea.creador = self._user
        tarea.joinity=self._joinity
        if commit:
            tarea.save()
        return tarea

class Anyadir_Lugar(forms.Form):
    lugar=forms.CharField()
    class Meta:
        model=Lugares_Tarea
        fields=("lugar")