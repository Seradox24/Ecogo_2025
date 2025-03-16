from django.urls import path , include
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('no_access/', no_access, name='no_access'),
    path('accounts/profile/', profile_view, name='profile'),
    

]
