### Este archivo define decoradores para restringir el acceso a vistas en función del perfil del usuario.
### Los decoradores verifican el perfil del usuario asociado al objeto `UsersMetadata`.
### Si el perfil coincide con el requerido, la vista se ejecuta; de lo contrario, el usuario es redirigido.
### Decoradores incluidos:
### - `Alumno_required`: Restringe acceso solo a usuarios con perfil de Alumno ('A').
### - `Docente_required`: Restringe acceso solo a usuarios con perfil de Docente ('D').
### - `Coordinador_required`: Restringe acceso solo a usuarios con perfil de Coordinador ('C').d

from functools import wraps
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import UsersMetadata

# Decorador para restringir acceso a usuarios con perfil 'Alumno'
def Alumno_required(view_func):
    @wraps(view_func)  # Preserva los metadatos de la función original
    @login_required  # Requiere que el usuario esté autenticado
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Obtiene los metadatos del usuario actual
            user_metadata = UsersMetadata.objects.get(user=request.user)
            
            # Verifica si el perfil es 'Alumno' ('A')
            if user_metadata.perfil == 'A':
                return view_func(request, *args, **kwargs)  # Ejecuta la vista original
            else:
                # Redirige a una vista de acceso denegado si el perfil no coincide
                return redirect(reverse('no_access'))
        except UsersMetadata.DoesNotExist:
            # Si no existen metadatos para el usuario, redirige al login
            return redirect('login')
    return _wrapped_view

# Decorador para restringir acceso a usuarios con perfil 'Docente'
def Docente_required(view_func):
    @wraps(view_func)  # Preserva los metadatos de la función original
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Obtiene los metadatos del usuario actual
            user_metadata = UsersMetadata.objects.get(user=request.user)

            # Verifica si el perfil es 'Docente' ('D')
            if user_metadata.perfil == 'D':
                return view_func(request, *args, **kwargs)  # Ejecuta la vista original
            else:
                # Redirige a una vista de acceso denegado si el perfil no coincide
                return redirect('no_access')
        except UsersMetadata.DoesNotExist:
            # Si no existen metadatos para el usuario, redirige al login
            return redirect('login')
    return _wrapped_view

# Decorador para restringir acceso a usuarios con perfil 'Coordinador'
def Coordinador_required(view_func):
    @wraps(view_func)  # Preserva los metadatos de la función original
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Obtiene los metadatos del usuario actual
            user_metadata = UsersMetadata.objects.get(user=request.user)

            # Verifica si el perfil es 'Coordinador' ('C')
            if user_metadata.perfil == 'C':
                return view_func(request, *args, **kwargs)  # Ejecuta la vista original
            else:
                # Redirige a una vista de acceso denegado si el perfil no coincide
                return redirect('no_access')
        except UsersMetadata.DoesNotExist:
            # Si no existen metadatos para el usuario, redirige al login
            return redirect('login')
    return _wrapped_view