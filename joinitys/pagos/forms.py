from django import forms
from models import Pagos

class PagosForm(forms.ModelForm):
    correo = forms.EmailField()
    nombre = forms.CharField()
    usuarios = forms.CheckboxSelectMultiple()
    precio = forms.DecimalField(localize=True)
    class Meta:
        model = Pagos
        fields = ('correo', 'nombre', 'usuarios', 'precio')
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._joinity=kwargs.pop('joinity')
        super(PagosForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        pago = super(PagosForm, self).save(commit=False)
        pago.creador = self._user
        pago.joinity= self._joinity
        if commit:
            pago.save()
            # self.save_m2m()
        return pago
        # pago.email = self.cleaned_data["email"]
        
        

