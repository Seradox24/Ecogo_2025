from django.contrib import admin
from .models import  Asignatura, UsersMetadata

admin.site.register(Asignatura)
admin.site.register(UsersMetadata)

# Register your models here.
admin.site.site_header = 'Administración Eco-Go'
admin.site.index_title = 'Administración Eco-Go'
admin.site.site_title = 'Administración Eco-Go'