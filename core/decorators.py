from functools import wraps
from django.shortcuts import render, redirect
from core.models import UsersMetadata
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def Alumno_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_metadata = UsersMetadata.objects.get(user=request.user)
            if user_metadata.perfil == 'A':
                return view_func(request, *args, **kwargs)
            else:
                
                return redirect(reverse('no_access')) # Redirige a una vista que indica que no tiene acceso
        except UsersMetadata.DoesNotExist:
            
            
            return redirect('login')  # Redirect to login page after logout
    return _wrapped_view

def Docente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_metadata = UsersMetadata.objects.get(user=request.user)
            if user_metadata.perfil == 'D':
                return view_func(request, *args, **kwargs)
            else:
                return redirect('no_access')  # Redirige a una vista que indica que no tiene acceso
        except UsersMetadata.DoesNotExist:
            # Si no existe el metadata, redirige a login o una página personalizada
            return redirect('login')  # O alguna otra vista que desees
    return _wrapped_view

def Coordinador_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_metadata = UsersMetadata.objects.get(user=request.user)
            if user_metadata.perfil == 'C':
                return view_func(request, *args, **kwargs)
            else:
                return redirect('no_access')  # Redirige a una vista que indica que no tiene acceso
        except UsersMetadata.DoesNotExist:
            # Si no existe el metadata, redirige a login o una página personalizada
            return redirect('login')  # O alguna otra vista que desees
    return _wrapped_view


# def Pañol_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         user_metadata = UsersMetadata.objects.get(user=request.user)
#         if user_metadata.perfil.nombre == 'Pañol':
#             return view_func(request, *args, **kwargs)
#         else:
#             return redirect('no_access')  # Redirige a una vista que indica que no tiene acceso
#     return _wrapped_view