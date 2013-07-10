from django import forms
from models import Amigos

class Invitar_Amigo(forms.ModelForm):
    
    class Meta:
        model = Amigos
        fields = ("amigo",)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(Invitar_Amigo, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nuevo_amigo = super(Invitar_Amigo, self).save(commit=False)
        nuevo_amigo.usuario = self._user
        if commit:
            nuevo_amigo.save()
            # self.save_m2m()
        return nuevo_amigo
        # pago.email = self.cleaned_data["email"]
        
