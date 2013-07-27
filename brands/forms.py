from django import forms
from models import Brand, Fotos, Puntuaciones

class EmpresaForm(forms.ModelForm):
    nombre=forms.CharField()
    notas=forms.CharField()
    tipo=forms.CharField()
    ubicacion=forms.CharField()
    video=forms.CharField()
    class Meta:
        model = Brand
        fields=("nombre", "notas", "precio", "tipo", "calificacion", "ubicacion", "imagen_cabecera", "video", "imagen_fondo",)
class Subir_Foto(forms.ModelForm):
    foto=forms.ImageField(required=False)
    class Meta:
        model=Fotos
        fields=("foto",)
    def __init__(self, *args, **kwargs):
        self._empresa=kwargs.pop('empresa')
        super(Subir_Foto, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        nueva=super(Subir_Foto, self).save(commit=False)
        nueva.empresa=self._empresa
        if commit:
            nueva.save()
        return nueva
class Puntuar(forms.ModelForm):
    puntuacion = forms.ChoiceField(choices=([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]), required=True)

    class Meta:
        model = Puntuaciones
        fields = ("puntuacion",)

    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._empresa = kwargs.pop('empresa')
        super(Puntuar, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nueva_puntuacion = super(Puntuar, self).save(commit=False)
        nueva_puntuacion.empresa = self._empresa
        nueva_puntuacion.usuario = self._usuario
        if commit:
            nueva_puntuacion.save()
            # self.save_m2m()
        return nueva_puntuacion