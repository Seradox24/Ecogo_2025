# from django.shortcuts import render
# from django.contrib.auth import authenticate, login as auth_login
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# import logging
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.

# def login(request):
#     logger = logging.getLogger(__name__)

#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('home'))

#     if request.method == 'POST':
#         try:
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 logger.info(f'User {username} authenticated successfully.')
#                 return HttpResponseRedirect(reverse('home'))
#             else:
#                 logger.warning(f'Failed authentication attempt for username: {username}')
#                 return render(request, 'acceso/login.html', {
#                     'error_message': 'Credenciales inválidas, inténtelo nuevamente o póngase en contacto con su coordinador.'
#                 })
#         except Exception as e:
#             logger.error(f'Error during authentication: {e}')
#             return render(request, 'acceso/login.html', {
#                 'error_message': 'Ocurrió un error durante la autenticación. Por favor, inténtelo de nuevo más tarde.'
#             })

#     return render(request, 'acceso/login.html')


from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from requests import request 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from alumno.views import home_alumno
from core.models import UsersMetadata
from django.contrib.auth import authenticate, login as auth_login
import logging


@user_passes_test(lambda user: not user.is_authenticated, login_url='accounts/profile/')
def login(request):
    

    logger = logging.getLogger(__name__)
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            logger.info(f'User {username} authenticated successfully.')
            return redirect('profile')
        else:
            logger.warning(f'Failed authentication attempt for username: {username}')
            error_message = 'Credenciales inválidas, inténtelo nuevamente o póngase en contacto con su coordinador.'

    return render(request, 'acceso/login.html', {'error_message': error_message})

   





@login_required
def profile_view(request):
    # Obtener el usuario actual
    user = request.user

    # Obtener el perfil del usuario desde UsersMetadata
    try:
        user_metadata = UsersMetadata.objects.get(user=user)

        # Verificar la condición del perfil
        if user_metadata.perfil == 'A':
            print('alumnito')
            return redirect('alumno:home_alumno')
        elif user_metadata.perfil == 'D':
            print('profe')
            return redirect('docente:home_docente')
        elif user_metadata.perfil == 'C':
            print('profe')
            return redirect('coordinador:home_coordinador')        
        else:
            # Puedes ajustar esta redirección según tus necesidades
            return render(request, '403', {'user': user})

    except UsersMetadata.DoesNotExist:
        logout(request)
        # Manejar el caso en el que no se encuentra el metadata del usuario
        return redirect('/')


def acceso_error(request):
    # Aquí puedes agregar el código para obtener la información del perfil del usuario
    # Por ejemplo, puedes obtener el usuario actual con request.user
    user = request.user

    # Luego puedes renderizar una plantilla con la información del perfil
    return render(request, 'acceso/login.html', {'user': user})


def no_access(request):
    return render(request, 'acceso/no_access.html')

def custom_404(request, exception):
    print('404 error ')
    return render(request, 'acceso/no_access.html', status=404)