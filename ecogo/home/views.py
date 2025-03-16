from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from core.decorators import Alumno_required
from core.models import UsersMetadata
from django.contrib.auth.decorators import user_passes_test


def home(request):

    
        
    return render(request, 'home/home.html')

 
