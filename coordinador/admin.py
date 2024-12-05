from django.contrib import admin
from .models import SalidaTerreno, DiaSemana

class SalidaTerrenoAdmin(admin.ModelAdmin):
    list_display = ('numero_cuenta', 'semestre', 'anio', 'semana', 'fecha_ingreso', 'fecha_termino', 'dias', 'noches', 'lugar_ejecucion', 'estado', 'actividad', 'exp_aprendizaje', 'semaforo', 'observaciones')
    list_filter = ('estado', 'semestre', 'actividad', 'semaforo', 'exp_aprendizaje', 'diasemana')
    search_fields = ('numero_cuenta', 'lugar_ejecucion', 'observaciones', 'exp_aprendizaje')
    date_hierarchy = 'fecha_ingreso'
    ordering = ('fecha_ingreso',)
    
    filter_vertical = ('asignaturas', 'secciones', 'docentes_apoyo', 'diasemana')  # Cambiado a filter_vertical para usar checkboxes
    
admin.site.register(SalidaTerreno, SalidaTerrenoAdmin)
admin.site.register(DiaSemana)  # Registra también el modelo DiaSemana si lo necesitas en el admin
