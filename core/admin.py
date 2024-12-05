from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UsersMetadata, UsersAcademy, Asignatura, NombreSeccion, Seccion, Inscripcion

class UsersMetadataInline(admin.StackedInline):
    model = UsersMetadata
    can_delete = False
    verbose_name_plural = 'Metadata del Usuario'

class UsersAcademyInline(admin.StackedInline):
    model = UsersAcademy
    can_delete = False
    verbose_name_plural = 'Información Académica'

class CustomUserAdmin(UserAdmin):
    inlines = (UsersMetadataInline, UsersAcademyInline)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sigla', 'coordinador', 'semestre')
    list_filter = ('semestre', 'coordinador')
    search_fields = ('nombre', 'sigla')

class NombreSeccionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class SeccionAdmin(admin.ModelAdmin):
    list_display = ('asignatura', 'nombre', 'docente', 'cupo')
    list_filter = ('asignatura', 'docente')
    search_fields = ('asignatura__nombre', 'nombre__nombre', 'docente__username')

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'seccion', 'fecha_inscripcion', 'estado')
    list_filter = ('estado', 'seccion__asignatura')
    search_fields = ('alumno__username', 'seccion__asignatura__nombre')
    date_hierarchy = 'fecha_inscripcion'



# Registrar todos los modelos con sus respectivas clases Admin
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(NombreSeccion, NombreSeccionAdmin)
admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)


# Register your models here.
admin.site.site_header = 'Administración Eco-Go'
admin.site.index_title = 'Administración Eco-Go'
admin.site.site_title = 'Administración Eco-Go'