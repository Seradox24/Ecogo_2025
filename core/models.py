from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    conctacto_sostenedor = models.CharField(max_length=100, blank=True, null=True)    
    
    
    

    def __str__(self):
        return f'{self.nombres} {self.ap_paterno} {self.ap_materno} '

    class Meta:
        verbose_name = 'User Metadata'
        verbose_name_plural = 'Users Metadata'



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

    TIPOINGRE_CHOICES = [
        ('ALUMNO DE INICIO', 'ALUMNO DE INICIO'),
        ('ALUMNO DE ADMISIÓN ESPECIAL', 'ALUMNO DE ADMISIÓN ESPECIAL'),
    ]

    SUBTIPO_INGRE_CHOICES = [
        ('REGULAR', 'REGULAR'),
        ('INTERNO', 'INTERNO'),
        ('RAP-IES', 'RAP-IES'),
        ('otro', 'otro'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usersAcademy')
    anno_ingreso = models.IntegerField(blank=True, null=True, choices=[(r, r) for r in range(2015, 2050)], verbose_name="Año de Ingreso")
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES, blank=True, null=True)
    cod_carrera = models.CharField(max_length=100, blank=True, null=True)
    nom_carrera = models.CharField(max_length=120, blank=True, null=True)
    tipo_ingreso = models.CharField(choices=TIPOINGRE_CHOICES, max_length=100, blank=True, null=True)
    subtipo_ingreso = models.CharField(choices=SUBTIPO_INGRE_CHOICES, max_length=100, blank=True, null=True)
    username_field = models.CharField(max_length=100, blank=True, null=True)
    correoduoc = models.EmailField(max_length=100, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    sede = models.CharField(max_length=100, blank=True, null=True)
    modalidad = models.CharField(max_length=100, blank=True, null=True)
    jornada = models.CharField(max_length=100, blank=True, null=True)
    asignaturas_inscritas = models.ManyToManyField('Asignatura', related_name='alumnos_inscritos', blank=True)

    def __str__(self):
        return f'{self.user.usersmetadata.nombres} {self.user.usersmetadata.ap_paterno} - {self.nom_carrera}'

    class Meta:
        verbose_name = 'User Academy'
        verbose_name_plural = 'Users Academy'

class Asignatura(models.Model):
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

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
    coordinador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='asignaturas_coordinadas')
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES, default=1)

    def __str__(self):
        return f"{self.get_semestre_display()}  -  {self.nombre}  -  Sigla {self.sigla} "

    class Meta:
        db_table = 'asignaturas'
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

class NombreSeccion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.ForeignKey(NombreSeccion, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True, default=None)
    docente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='secciones_impartidas')
    cupo = models.IntegerField(default=30)

    def __str__(self):
        return f"( {self.nombre} - {self.docente.usersmetadata.nombres} {self.docente.usersmetadata.ap_paterno} - {self.asignatura.nombre} )"

    class Meta:
        db_table = 'secciones'
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'

    def espacios_disponibles(self):
        return self.cupo - self.inscripciones.count()
    
    def cantidad_alumnos(self):
        return self.inscripciones.count()
    
  

class Inscripcion(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('ACTIVA', 'Activa'),
        ('FINALIZADA', 'Finalizada'),
        ('RETIRADA', 'Retirada')
    ])

    class Meta:
        unique_together = ('alumno', 'seccion')

    def clean(self):
        if self.alumno.usersmetadata.perfil != 'A':
            raise ValidationError('Solo los alumnos pueden inscribirse en secciones.')
        if Inscripcion.objects.filter(
            alumno=self.alumno,
            seccion__asignatura=self.seccion.asignatura
        ).exclude(pk=self.pk).exists():
            raise ValidationError('El alumno ya está inscrito en otra sección de esta asignatura.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Actualizar UsersAcademy
        users_academy, created = UsersAcademy.objects.get_or_create(user=self.alumno)
        users_academy.asignaturas_inscritas.add(self.seccion.asignatura)

    def __str__(self):
        return f"{self.alumno.usersmetadata.nombres} - {self.seccion}"



