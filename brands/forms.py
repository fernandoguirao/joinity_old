from django import forms
from models import Brand, Fotos, Puntuaciones
from datetime import date
from joinitys.models import Reservas_Joinity
class BrandForm(forms.ModelForm):
    nombre=forms.CharField()
    direccion=forms.CharField()
    web=forms.CharField()
    tipo=forms.CharField()
    ubicacion=forms.CharField()
    video=forms.CharField(required=False)
    telefono=forms.IntegerField()
    class Meta:
        model = Brand
        fields=("nombre", "direccion", "web", "tipo", "ubicacion", "video", "telefono", "imagen_cabecera", "imagen_fondo")
        #fields=("nombre", "direccion", "tipo", "web", "calificacion", "ubicacion", "imagen_cabecera", "video", "imagen_fondo","telefono")
        
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

class ReservaRestaurante(forms.ModelForm):
    fecha_inicio=forms.DateField(widget=forms.TextInput(attrs={'class':'span2 hasDatepicker inputNormal', 'id':'datepicker-01', 'value':str(date.today())}))
    hora=forms.ChoiceField(widget=forms.Select(attrs={'class':'select span1'}), choices=([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12"),("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"),("18","18"),("19","19"),("20","20"),("21","21"),("22","22"),("23","23"),("24","24")]))
    minuto=forms.ChoiceField(widget=forms.Select(attrs={'class':'select span1'}), choices=([("0","00"),("15","15"),("30","30"),("45","45")]))
    notas=forms.CharField(widget=forms.TextInput(attrs={'class':'inputNormal'}))
    n_personas=forms.IntegerField(widget=forms.TextInput(attrs={'class':'inputNormal'}))
    class Meta:
        model = Reservas_Joinity
        fields = ("fecha_inicio", "notas", "n_personas")
    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._brand = kwargs.pop('brand')
        self._joinity=kwargs.pop('joinity')
        super(ReservaRestaurante, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        nueva_reserva=super(ReservaRestaurante, self).save(commit=False)
        nueva_reserva.brand = self._brand
        nueva_reserva.usuario = self._usuario
        nueva_reserva.joinity = self._joinity
        if commit:
            nueva_reserva.save()
            # self.save_m2m()
        return nueva_reserva
class ReservaHotel(forms.ModelForm):
    fecha_inicio=forms.DateField(widget=forms.TextInput(attrs={'class':'span2 hasDatepicker inputNormal', 'id':'datepicker-01', 'value':str(date.today())}))
    hora_inicio=forms.ChoiceField(widget=forms.Select(attrs={'class':'select span1'}), choices=([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12"),("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"),("18","18"),("19","19"),("20","20"),("21","21"),("22","22"),("23","23"),("24","24")]))
    minuto_inicio=forms.ChoiceField(widget=forms.Select(attrs={'class':'select span1'}), choices=([("00","00"),("15","15"),("30","30"),("45","45")]))
    fecha_fin=forms.DateField(widget=forms.TextInput(attrs={'class':'span2 hasDatepicker inputNormal', 'id':'datepicker-02', 'value':str(date.today())}))
    hora_fin=forms.ChoiceField(widget=forms.Select(attrs={'class':'select span1'}), choices=([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12"),("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"),("18","18"),("19","19"),("20","20"),("21","21"),("22","22"),("23","23"),("24","24")]))
    minuto_fin=forms.ChoiceField(widget=forms.Select(attrs={'class':'select span1'}), choices=([("00","00"),("15","15"),("30","30"),("45","45")]))
    n_personas=forms.IntegerField(widget=forms.TextInput(attrs={'class':'inputNormal'}))
    n_habitaciones=forms.IntegerField(widget=forms.TextInput(attrs={'class':'inputNormal'}))
    class Meta:
        model = Reservas_Joinity
        fields = ("fecha_inicio", "fecha_fin", "n_personas", "n_habitaciones")
    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        self._brand = kwargs.pop('brand')
        self._joinity=kwargs.pop('joinity')
        super(ReservaHotel, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        nueva_reserva=super(ReservaHotel, self).save(commit=False)
        nueva_reserva.brand = self._brand
        nueva_reserva.usuario = self._usuario
        nueva_reserva.joinity = self._joinity
        if commit:
            nueva_reserva.save()
            # self.save_m2m()
        return nueva_reserva
    