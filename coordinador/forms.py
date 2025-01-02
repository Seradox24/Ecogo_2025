#--------- import form usuarios
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import UsersMetadata,UsersAcademy
from core.models import  Asignatura, Seccion, UsersMetadata
from .models import SalidaTerreno, DiaSemana
#--------- import form salidas


class UserCreationWithMetadataForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingresa una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Definir widgets personalizados con Tailwind
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
            'placeholder': 'Nombre de usuario'
        }))
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
            'placeholder': 'Correo electrónico'
        }))
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
            'placeholder': 'Contraseña'
        }))
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
            'placeholder': 'Confirmar contraseña'
        }))
    
    
class UsersMetadataForm(forms.ModelForm):
    username_field = forms.CharField(required=False, widget=forms.HiddenInput())  # Campo adicional opcional para capturar el nombre de usuario.

    class Meta:
        model = UsersMetadata
        fields = [
            'sexo', 'perfil', 'rut', 'nombres', 'ap_paterno', 'ap_materno',
            'fnacimiento', 'estado_civil', 'direccion', 'numero', 'celular', 'foto', 'conctacto_sostenedor'
        ]
        widgets = {
            'sexo': forms.Select(attrs={'class': 'form-select rounded border-gray-300'}),  # Campo con opciones definidas en `SEXO_CHOICES`.
            'perfil': forms.Select(attrs={'class': 'form-select border-gray-300'}),  # Campo con opciones definidas en `PERFIL_CHOICES`.
            'rut': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': '12345678-9'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Nombres completos'}),
            'ap_paterno': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Apellido paterno'}),
            'ap_materno': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Apellido materno'}),
            'fnacimiento': forms.DateInput(attrs={'class': 'form-control border-gray-300', 'type': 'date'}),
            'estado_civil': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Estado civil'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Dirección completa'}),
            'numero': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Número de casa/departamento'}),
            'celular': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': '+56912345678'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control border-gray-300'}),
            'conctacto_sostenedor': forms.TextInput(attrs={'class': 'form-control border-gray-300', 'placeholder': 'Numero de contacto de emergencia o sostenedor'}),
        }
        labels = {
            'sexo': '',
            'perfil': '',
            'rut': '',
            'nombres': '',
            'ap_paterno': '',
            'ap_materno': '',
            'fnacimiento': '',
            'estado_civil': '',
            'direccion': '',
            'numero': '',
            'celular': '',
            'foto': '',
            #
            'conctacto_sostenedor': '',
        }

#--------- formularios de usuarios academy

class UsersAcademyForm(forms.ModelForm):
    class Meta:
        model = UsersAcademy
        fields = [
            'semestre', 'sede', 'nom_carrera', 'modalidad', 'jornada', 'asignaturas_inscritas','anno_ingreso','cod_carrera','tipo_ingreso',
            'subtipo_ingreso', 'username_field', 'correoduoc', 'correo'
        ]
        widgets = {
            'semestre': forms.Select(attrs={'class': 'form-select'}),  # Campo con opciones definidas en `SEMESTRE_CHOICES`.
            'sede': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sede académica'}),
            'nom_carrera': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la carrera'}),
            'modalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modalidad (Ej: Presencial)'}),
            'jornada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jornada (Ej: Diurna, Vespertina)'}),
            'asignaturas_inscritas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input '}),
            'anno_ingreso': forms.Select(attrs={'class': 'form-select'}),  # Campo con opciones definidas en `SEMESTRE_CHOICES`.
            'cod_carrera': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de la carrera'}),
            'tipo_ingreso': forms.Select(attrs={'class': 'form-select'}),  # Campo con opciones definidas en `TIPOINGRE_CHOICES`.
            'subtipo_ingreso': forms.Select(attrs={'class': 'form-select'}),  # Campo con opciones definidas en `SUBTIPO_INGRE_CHOICES`.
            'username_field': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'correoduoc': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo DUOC'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo personal'}),
        }
        labels = {
            'semestre': '',
            'sede': '',
            'nom_carrera': '',
            'modalidad': '',
            'jornada': '',
            'asignaturas_inscritas': '',
            #
            'anno_ingreso': '',
            'cod_carrera': '',
            'tipo_ingreso': '',
            'subtipo_ingreso': '',
            'username_field': '',
            'correoduoc': '',
            'correo': '',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar las asignaturas por semestre
        self.fields['asignaturas_inscritas'].queryset = Asignatura.objects.all().order_by('semestre')






#--------- formularios de salidas



class SalidaTerrenoForm(forms.ModelForm):
    class Meta:
        model = SalidaTerreno
        fields = [
            'estado', 'activo', 'numero_cuenta', 'semestre', 'anio', 'semana', 'diasemana', 'actividad',
            'fecha_ingreso', 'fecha_termino', 'dias', 'noches', 'lugar_ejecucion', 'asignaturas', 'exp_aprendizaje',
            'secciones', 'docentes_apoyo', 'num_salida', 'observaciones', 'semaforo'
        ]
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select border-gray-300'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero_cuenta': forms.NumberInput(attrs={'class': 'form-control border-gray-300'}),
            'semestre': forms.Select(attrs={'class': 'form-select border-gray-300'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control border-gray-300'}),
            'semana': forms.NumberInput(attrs={'class': 'form-control border-gray-300'}),
            'diasemana': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'actividad': forms.TextInput(attrs={'class': 'form-control border-gray-300'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control border-gray-300', 'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'class': 'form-control border-gray-300', 'type': 'date'}),
            'dias': forms.NumberInput(attrs={'class': 'form-control border-gray-300'}),
            'noches': forms.NumberInput(attrs={'class': 'form-control border-gray-300'}),
            'lugar_ejecucion': forms.TextInput(attrs={'class': 'form-control border-gray-300'}),
            'asignaturas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'exp_aprendizaje': forms.Select(attrs={'class': 'form-select border-gray-300'}),
            'secciones': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'docentes_apoyo': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'num_salida': forms.Select(attrs={'class': 'form-select border-gray-300'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control border-gray-300'}),
            'semaforo': forms.Select(attrs={'class': 'form-select border-gray-300'}),
        }
        labels = {
            'estado': '',
            'activo': '',
            'numero_cuenta': '',
            'semestre': '',
            'anio': '',
            'semana': '',
            'diasemana': '',
            'actividad': '',
            'fecha_ingreso': '',
            'fecha_termino': '',
            'dias': '',
            'noches': '',
            'lugar_ejecucion': '',
            'asignaturas': '',
            'exp_aprendizaje': '',
            'secciones': '',
            'docentes_apoyo': '',
            'num_salida': '',
            'observaciones': '',
            'semaforo': '',
        }

    def __init__(self, *args, **kwargs):
        super(SalidaTerrenoForm, self).__init__(*args, **kwargs)
        self.fields['diasemana'].queryset = DiaSemana.objects.all().order_by('id')
        self.fields['diasemana'].label_from_instance = lambda obj: obj.nombre
        self.fields['asignaturas'].queryset = Asignatura.objects.all().order_by('semestre', 'nombre')
        self.fields['secciones'].queryset = Seccion.objects.all().order_by('asignatura', 'nombre')
        self.fields['docentes_apoyo'].queryset = UsersMetadata.objects.filter(perfil='D').order_by('nombres')



  
        
        if self.instance and self.instance.fecha_ingreso:
            self.fields['fecha_ingreso'].widget.attrs['value'] = self.instance.fecha_ingreso.strftime('%Y-%m-%d')
        if self.instance and self.instance.fecha_termino:
            self.fields['fecha_termino'].widget.attrs['value'] = self.instance.fecha_termino.strftime('%Y-%m-%d')




#--------- formularios de asignaturas

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'sigla', 'coordinador', 'semestre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control border-gray-300'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control border-gray-300'}),
            'coordinador': forms.Select(attrs={'class': 'form-select border-gray-300'}),
            'semestre': forms.Select(attrs={'class': 'form-select border-gray-300'}),
        }
        labels = {
            'nombre': '',
            'sigla': '',
            'coordinador': '',
            'semestre': '',
        }

    def __init__(self, *args, **kwargs):
        super(AsignaturaForm, self).__init__(*args, **kwargs)
        self.fields['coordinador'].queryset = User.objects.filter(usersmetadata__perfil='C').order_by('username')
        self.fields['coordinador'].label_from_instance = lambda obj: f'{obj.usersmetadata.nombres} {obj.usersmetadata.ap_paterno}'
        self.fields['semestre'].widget.choices = Asignatura.SEMESTRE_CHOICES
        