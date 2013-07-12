from django import forms
from models import Eventos, Lugares_Evento
from datetime import date
class Crear_Evento(forms.ModelForm):
    titulo=forms.CharField()
    foto = forms.ImageField(required=False)
    privacidad=forms.ChoiceField(choices=([("0", "Publico"), ("1", "Privado")]))
    privilegios=forms.ChoiceField(choices=([("0", "Solo administrador"), ("1", "Todos los participantes")]))
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    fecha_inicio=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-01', 'value':str(date.today())}))
    fecha_fin=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-01', 'value':str(date.today())}))

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