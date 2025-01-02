from django.core.validators import MaxValueValidator
from django.db import models
from core.models import *

class DiaSemana(models.Model):
    nombre = models.CharField(max_length=100)

# Definir los choices para los campos que los requieren
SEMAFORO_CHOICES = [
    ('verde', 'Confirmado'),
    ('amarillo', 'Viable'),
    ('rojo', 'Poco fiable'),
    ('gris', 'Por confirmar'),
]

EXP_APRENDIZAJE_CHOICES = [
    ('EA-1', 'EA-1'),
    ('EA-2', 'EA-2'),
    ('EA-3', 'EA-3'),
    ('EA-4', 'EA-4'),
    ('examen_transversal', 'Examen Transversal'),
    ('por_definir', 'Por definir'),  # Se agrega por defecto
]

ACTIVIDAD_CHOICES = [
    ('actividad_1', 'Actividad 1'),
    ('actividad_2', 'Actividad 2'),
    ('actividad_3', 'Actividad 3'),
    ('actividad_4', 'Actividad 4'),
    ('por_definir', 'Por definir'),  # Se agrega por defecto
]

ESTADO_CHOICES = [
    ('EJECUTADO', 'Ejecutado'),
    ('POR_EJECUTAR', 'Por Ejecutar'),
    ('por_definir', 'Por definir'),  # Se agrega por defecto
]

SEMESTRE_CHOICES = [
    (1, '1 Semestre'),
    (2, '2 Semestre'),
    (3, '3 Semestre'),
    (4, '4 Semestre'),
    (5, '5 Semestre'),
    (6, '6 Semestre'),
    (7, '7 Semestre'),
    (8, '8 Semestre'),
]

class SalidaTerreno(models.Model):
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='por_definir')  # Default agregado
    activo = models.BooleanField(default=True)  # Campo booleano para activar/desactivar
    numero_cuenta = models.IntegerField()
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES, blank=True, null=True)
    anio = models.PositiveIntegerField(validators=[MaxValueValidator(3000)], blank=True, null=True)
    semana = models.PositiveIntegerField(validators=[MaxValueValidator(3000)], blank=True, null=True)
    diasemana = models.ManyToManyField(DiaSemana, blank=True)
    actividad = models.CharField(max_length=200, blank=True, null=True, default='por_definir')
    fecha_ingreso = models.DateField()
    fecha_termino = models.DateField()
    dias = models.PositiveIntegerField(validators=[MaxValueValidator(99)], blank=True, null=True, default=0) 
    noches = models.PositiveIntegerField(validators=[MaxValueValidator(99)],blank=True, null=True, default=0)
    lugar_ejecucion = models.CharField(max_length=60)
    asignaturas = models.ManyToManyField(Asignatura, related_name='salidas_terreno', blank=True)
    exp_aprendizaje = models.CharField(max_length=20, choices=EXP_APRENDIZAJE_CHOICES, blank=True, null=True, default='por_definir')
    secciones = models.ManyToManyField(Seccion, blank=True)
    docentes_apoyo = models.ManyToManyField(UsersMetadata, related_name='salidas_terreno_apoyo', blank=True)
    num_salida = models.CharField(max_length=30, choices=[(str(i), str(i)) for i in range(1, 5)] + [('no_requiere', 'No Requiere')], blank=True, null=True)
    observaciones = models.TextField()
    semaforo = models.CharField(max_length=20, choices=SEMAFORO_CHOICES, blank=True, null=True)
    

    def __str__(self):
        asignaturas_str = ', '.join([asignatura.nombre for asignatura in self.asignaturas.all()])
        return f"Salida a terreno de {asignaturas_str} - {self.fecha_ingreso}"
    
    def asignaturas_x_seccion(self):
        """
        Retorna un diccionario con las asignaturas y la cantidad de secciones asociadas a este viaje.
        """
        from django.db.models import Count

        try:
            asignaturas_secciones = self.secciones.values('asignatura__nombre').annotate(total_secciones=Count('id'))
            data = {item['asignatura__nombre']: item['total_secciones'] for item in asignaturas_secciones}

            # Agregar asignaturas sin secciones
            asignaturas_sin_secciones = self.asignaturas.exclude(nombre__in=data.keys())
            for asignatura in asignaturas_sin_secciones:
                data[asignatura.nombre] = 'Sin secciones asignadas'

            # Verificar secciones sin asignaturas
            secciones_sin_asignaturas = self.secciones.filter(asignatura__isnull=True)
            if secciones_sin_asignaturas.exists():
                data['Secciones sin asignatura'] = 'Existen secciones sin asignatura asignada'

            return data
        except Exception as e:
            # Log the exception if needed
            return {}

    def get_asignaturas_secciones_list(self):
        """
        Retorna una lista de tuplas con las asignaturas y la cantidad de secciones asociadas a este viaje.
        """
        try:
            data = self.asignaturas_x_seccion()
            return [(asignatura, total_secciones) for asignatura, total_secciones in data.items()]
        except Exception as e:
            # Log the exception if needed
            return []


    class Meta:
        verbose_name = 'Salida Terreno'
        verbose_name_plural = 'Salidas Terreno'
