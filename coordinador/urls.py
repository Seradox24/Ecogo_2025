from django.urls import path
from .views import *

app_name = 'coordinador'

urlpatterns = [
    #home coordinador
    path('',home_coordinador , name='home_coordinador'),
    #usuarios
    path('crear-usuario/', crear_usuario, name='crear-usuario'),
    #salidas
    path('listar-salida/', listar_salida, name="listar_salida"),
]


