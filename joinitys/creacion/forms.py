from django import forms
from joinitys.models import Joinitys, Compras, Aficiones, Family, Lugares_Joinity
from datetime import date

class JoinityForm(forms.ModelForm):
    nombre=forms.CharField(widget=forms.Textarea(attrs={"class":"inputNormal input-small","placeholder":"Ejemplo: '80 cumpleanos de la abuela' o 'Clases de natacion para principiantes'"}))
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"inputNormal input-small","placeholder":""}))
    foto=forms.ImageField(required=False,widget=forms.FileInput({"class":"inputFoto","id":"fotoinput"}))
    n_min=forms.IntegerField(required=False)
    n_max=forms.IntegerField(required=False)
    precio = forms.DecimalField(localize=True, required=False)
    #usuarios = forms.CheckboxSelectMultiple()
    privacidad=forms.ChoiceField(choices=([("0", "Publico"), ("1","Peticion de invitacion"), ("2", "Privado")]))
    class Meta:
        model = Joinitys
        fields = ('nombre','descripcion', 'n_min', 'n_max', 'precio', 'privacidad', 'foto')
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._tipo = kwargs.pop('tipo')
        super(JoinityForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        joinity = super(JoinityForm, self).save(commit=False)
        joinity.creador = self._user
        joinity.tipo=self._tipo
        if commit:
            if not joinity.n_min:
                joinity.n_min=0
            if not joinity.n_max:
                joinity.n_max=0
            joinity.save()
            # self.save_m2m()
        return joinity

class FamilyForm(forms.ModelForm):
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    fecha_inicio=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-01', 'value':str(date.today())}))
    fecha_fin=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-02', 'value':str(date.today())}))
    class Meta:
        model = Family
        fields=("subcategoria", "fecha_inicio", "fecha_fin", "repeticion")
    def __init__(self, *args, **kwargs):
        self._joinity = kwargs.pop('joinity')
        super(FamilyForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        family = super(FamilyForm, self).save(commit=False)
        family.joinity = self._joinity
        if commit:
            family.save()
        return family
class AficionesForm(forms.ModelForm):
    repeticion = forms.ChoiceField(choices=([("0", "Puntual"), ("1", "Diario"), ("2", "Semanal"), ("3", "2 Semanas"), ("4", "Mensual"), ("5", "Anual")]), required=True)
    nivel = forms.ChoiceField(choices=([("0", "Indiferente"), ("1", "Amateur"), ("2", "Intermedio"), ("3", "Pro")]), required=True)
    fecha_inicio=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-01', 'value':str(date.today())}))
    fecha_fin=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-02', 'value':str(date.today())}))
    requisitos=forms.CharField(required=False)
    class Meta:
        model = Aficiones
        fields=("subcategoria", "fecha_inicio", "fecha_fin", "repeticion", "nivel", "requisitos")
    def __init__(self, *args, **kwargs):
        self._joinity = kwargs.pop('joinity')
        super(AficionesForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        aficion = super(AficionesForm, self).save(commit=False)
        aficion.joinity = self._joinity
        if commit:
            if not aficion.requisitos:
                aficion.requisitos="Sin requisitos"
            aficion.save()
        return aficion
        # pago.email = self.cleaned_data["email"]
class ComprasForm(forms.ModelForm):
    fecha_fin=forms.DateField(widget=forms.TextInput(attrs={'class':'span2', 'id':'datepicker-01', 'value':str(date.today())}))
    class Meta:
        model = Compras
        fields=("subcategoria", "n_descuento1", "descuento1", "n_descuento2", "descuento2", "n_descuento3", "descuento3", "envio", "fecha_fin", "iva", "brand")
    def __init__(self, *args, **kwargs):
        self._joinity = kwargs.pop('joinity')
        super(ComprasForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        compras = super(ComprasForm, self).save(commit=False)
        compras.joinity = self._joinity
        if commit:
            compras.save()
        return compras
class Anyadir_Lugar(forms.Form):
    lugar=forms.CharField()
    class Meta:
        model=Lugares_Joinity
        fields=("lugar")