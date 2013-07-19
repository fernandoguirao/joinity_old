from django import forms
from models import Puntuaciones, Usuarios
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"inputNormal input-small inputNombre","placeholder":"Tu nombre"}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"inputNormal input-small inputApellido","placeholder":"Tus apellidos"}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={"class":"inputNormal input-small","placeholder":"email@ejemplo.com"}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class PerfilForm(forms.ModelForm):
    dni = forms.CharField(required=False)
    universidad = forms.CharField(required=False)
    empresa = forms.CharField(required=False)
    ciudad = forms.CharField(required=True)
    foto = forms.ImageField(required=False)
    telefono = forms.IntegerField(required=False)
    nacimiento = forms.DateField(required=False)
    cpostal = forms.IntegerField(required=False)
    sexo = forms.ChoiceField(choices=([("0", "Hombre"), ("1", "Mujer")]), required=True)
    ocultar_perfil = forms.ChoiceField(choices=([("0", "No"), ("1", "Si")]))
    visible = forms.ChoiceField(choices=(["1", "Si"], ["0", "No"]))
    ubicacion_visible = forms.ChoiceField(choices=(["1", "Si"], ["0", "No"]))
    avisar = forms.ChoiceField(choices=(["1", "Si"], ["0", "No"]))
    class Meta:
        model = Usuarios
        fields = ('foto', 'dni', 'telefono', 'universidad', 'empresa', 'ciudad', 'nacimiento', 'sexo', 'cpostal', 'intereses', 'intereses_comprar', 'ocultar_perfil', 'visible', 'avisar', 'ubicacion_visible')

class Puntuar(forms.ModelForm):
    puntuacion = forms.ChoiceField(choices=([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]), required=True)

    class Meta:
        model = Puntuaciones
        fields = ("puntuacion",)

    def __init__(self, *args, **kwargs):
        self._puntuador = kwargs.pop('puntuador')
        self._puntuado = kwargs.pop('puntuado')
        super(Puntuar, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nueva_puntuacion = super(Puntuar, self).save(commit=False)
        nueva_puntuacion.puntuador = self._puntuador
        nueva_puntuacion.usuario = self._puntuado
        if commit:
            nueva_puntuacion.save()
            # self.save_m2m()
        return nueva_puntuacion
        # pago.email = self.cleaned_data["email"]
class Buscar(forms.Form):
    input = forms.CharField()
    filtro = forms.ChoiceField(choices=([("1", "Nombre"), ("2", "Ubicacion"), ("3", "Fecha de nacimiento"), ("4", "Email"), ("5", "Intereses")]))
    
    
