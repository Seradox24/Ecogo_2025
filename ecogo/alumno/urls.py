from django.urls import path , include
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'alumno'

urlpatterns = [
    path('',home_alumno , name='home_alumno'),

    

]
