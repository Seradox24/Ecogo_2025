from django.shortcuts import render

from core.decorators import Docente_required

# Create your views here.

@Docente_required
def home_docente(request):
    print('home_docente')
    return render(request, 'docente/home_docente.html')