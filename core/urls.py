from django.urls import path
from .views import *

from django.conf.urls import handler403
from .views import error_403_view

handler403 = error_403_view


urlpatterns = [
    path('403/', error_403_view, name='403'),
    

]

