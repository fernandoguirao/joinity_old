# -*- encoding: utf-8 -*-

from django import forms
from models import Mensajes

class Mandar_Mensaje_Form(forms.ModelForm):
    mensaje=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Dile algo a tu amigo.', 'id':'appendedInputButton-02', 'class':'span2'}))
    class Meta:
        model = Mensajes
        fields = ("mensaje",)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._destinatario=kwargs.pop('destinatario')
        super(Mandar_Mensaje_Form, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        mensaje = super(Mandar_Mensaje_Form, self).save(commit=False)
        mensaje.remitente = self._user
        mensaje.destinatario=self._destinatario
        mensaje.asunto="sin"
        if commit:
            mensaje.save()
            # self.save_m2m()
        return mensaje
        # pago.email = self.cleaned_data["email"]
        
