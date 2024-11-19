from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import UsersMetadata,UsersAcademy



class UserCreationWithMetadataForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingresa una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Definir widgets personalizados con Tailwind
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Nombre de usuario'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Correo electrónico'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Contraseña'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input mt-1 block w-full border-gray-300 rounded-md',
        'placeholder': 'Confirmar contraseña'
    }))
    
    
    




class UsersMetadataForm(forms.ModelForm):
    username_field = forms.CharField(required=False, widget=forms.HiddenInput())  # Campo adicional opcional para capturar el nombre de usuario.

    class Meta:
        model = UsersMetadata
        fields = [
            'sexo', 'perfil', 'rut', 'nombres', 'ap_paterno', 'ap_materno',
            'fnacimiento', 'estado_civil', 'direccion', 'numero', 'celular', 'foto'
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
        }
        labels = {
            'sexo': 'Sexo',
            'perfil': 'Perfil de usuario',
            'rut': 'RUT',
            'nombres': 'Nombres',
            'ap_paterno': 'Apellido paterno',
            'ap_materno': 'Apellido materno',
            'fnacimiento': 'Fecha de nacimiento',
            'estado_civil': 'Estado civil',
            'direccion': 'Dirección',
            'numero': 'Número',
            'celular': 'Teléfono celular',
            'foto': 'Foto de perfil',
        }


class UsersAcademyForm(forms.ModelForm):
    class Meta:
        model = UsersAcademy
        fields = [
            'semestre', 'sede', 'nom_carrera', 'modalidad', 'jornada', 'asignaturas_inscritas'
        ]
        widgets = {
            'semestre': forms.Select(attrs={'class': 'form-select'}),  # Campo con opciones definidas en `SEMESTRE_CHOICES`.
            'sede': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sede académica'}),
            'nom_carrera': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la carrera'}),
            'modalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modalidad (Ej: Presencial)'}),
            'jornada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jornada (Ej: Diurna, Vespertina)'}),
            'asignaturas_inscritas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'semestre': 'Semestre académico',
            'sede': 'Sede',
            'nom_carrera': 'Nombre de la carrera',
            'modalidad': 'Modalidad de estudio',
            'jornada': 'Jornada',
            'asignaturas_inscritas': 'Asignaturas inscritas',
        }
