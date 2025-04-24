from django.urls import path
from .views import *

app_name = 'coordinador'

urlpatterns = [
    #home coordinador
    path('',home_coordinador , name='home_coordinador'),
    #usuarios
    path('crear-usuario/', crear_usuario, name='crear-usuario'),
    path('editar-usuario/<int:id>/', editar_usuario, name='editar-usuarios'),
    path('listar-usuario/', listar_usuario, name='listar-usuario'),
    path('lista-usuarios/', lista_usuarios, name='lista-usuarios'), 
    #Gestionar salidas
    path('listar-salida/', listar_salida, name="listar_salida"),
    path('crear-salida/', crear_salida, name="crear_salida"),
    path('editar-salida/<int:id>/', editar_salida, name="editar_salida"),
    path('eliminar-salida/<int:id>/', eliminar_salida, name="eliminar_salida"),
    path('obtener-secciones/', obtener_secciones, name='obtener_secciones'),
    path('msj-wsp/', crear_grupo_wsp, name='crear_grupo_wsp'),
    #Gestionar alumnos
    #path('listar-alumno/', listar_alumno, name="listar_alumno"),

    #gestionar asignaturas
    path('listar-asignatura/', listar_asignatura, name="listar_asignatura"),
    path('crear-asignatura/', crear_asignatura, name="crear_asignatura"),
    path('editar-asignatura/<int:id>/', editar_asignatura, name="editar_asignatura"),
    path('eliminar-asignatura/<int:id>/', eliminar_asignatura, name="eliminar_asignatura"),
    

]


