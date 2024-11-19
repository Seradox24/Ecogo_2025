from django.shortcuts import render

from core.decorators import Alumno_required

# Create your views here.


@Alumno_required
def home_alumno(request):
    print('home_alumno')
    return render(request, 'alumno/home_alumno.html')