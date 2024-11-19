from django.urls import path
from .views import *

app_name = 'coordinador'

urlpatterns = [
    path('crear-usuario/', crear_usuario, name='crear-usuario'),
    path('',home_coordinador , name='home_coordinador'),
]


