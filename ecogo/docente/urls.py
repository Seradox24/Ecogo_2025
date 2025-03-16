from django.urls import path , include
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'docente'

urlpatterns = [
    path('',home_docente , name='home_docente'),

    

]