from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UsersMetadata(models.Model):

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    PERFIL_CHOICES = [
        ('A', 'Alumno'),
        ('C', 'Coordinador'),
        ('D', 'Docente'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usersmetadata')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    perfil = models.CharField(max_length=1, choices=PERFIL_CHOICES)
    foto = models.ImageField(upload_to='usuarios', blank=True, null=True)
    rut = models.CharField(max_length=100, blank=True, null=True, unique=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    ap_paterno = models.CharField(max_length=100, blank=True, null=True)
    ap_materno = models.CharField(max_length=100, blank=True, null=True)
    fnacimiento = models.DateField(blank=True, null=True)
    estado_civil = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return f'{self.nombres} {self.ap_paterno} {self.ap_materno} '

    class Meta:
        verbose_name = 'User Metadata'
        verbose_name_plural = 'Users Metadata'

class Asignatura(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)


    def __str__(self):
        return f"{self.nombre} - Sigla {self.sigla} "

    class Meta:
        db_table = 'asignaturas'
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'


class UsersAcademy(models.Model):

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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usersAcademy')
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES, blank=True, null=True)
    sede = models.CharField(max_length=100, blank=True, null=True)
    nom_carrera = models.CharField(max_length=100, blank=True, null=True)
    modalidad = models.CharField(max_length=100, blank=True, null=True)
    jornada = models.CharField(max_length=100, blank=True, null=True)
    asignaturas_inscritas = models.ManyToManyField(Asignatura, related_name='alumnos_inscritos', blank=True)