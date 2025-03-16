from django.shortcuts import render

# Create your views here.


def error_403_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)
