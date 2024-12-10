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
    path('crear-salida/', crear_salida, name="crear_salida"),
    path('editar-salida/<int:id>/', editar_salida, name="editar_salida"),
    path('eliminar-salida/<int:id>/', eliminar_salida, name="eliminar_salida"),
]


