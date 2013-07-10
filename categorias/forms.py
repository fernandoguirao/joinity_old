from django import forms
from models import Subcategorias, Subcategorias_Compras

class NuevoInteresForm(forms.ModelForm):
    nombre = forms.CharField()
    class Meta:
        model = Subcategorias
        fields = ("categoria", "nombre",)
class NuevaCompraForm(forms.ModelForm):
    nombre = forms.CharField()
    class Meta:
        model = Subcategorias_Compras
        fields = ("categoria", "nombre",)
        
