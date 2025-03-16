
# import de librerias generales
from itertools import count
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import requests
from core.decorators import Coordinador_required
from core.models import Inscripcion , Asignatura, Seccion, UsersAcademy, UsersMetadata
from django.db.models import Q
# import de librerias crear usuarios
from .forms import AsignaturaForm, UserCreationWithMetadataForm, UsersMetadataForm, UsersAcademyForm
# import de librerias listar salidas
from coordinador.models import SalidaTerreno
from .forms import SalidaTerrenoForm
from django.shortcuts import get_object_or_404, redirect


#home coordinador -------------------------------------------------------------------------------------
@login_required
@Coordinador_required
def home_coordinador(request):
    # Obtener la cantidad alumnos,salidas,asignaturas,secciones
    try:
        
        total_alumnos = UsersMetadata.objects.filter(perfil='A').count()
        total_salidas = SalidaTerreno.objects.count()
        salidas_activas = SalidaTerreno.objects.filter(activo=True, estado='POR_EJECUTAR')
        total_asignaturas = Asignatura.objects.count()
        total_seccionesv = Seccion.objects.count()

        # Obtener asignaturas activas y el conteo de secciones

       
        asignaturas_secciones_data = []  # Lista para almacenar la información de asignaturas y secciones

        for salida in salidas_activas:
            asignaturas_secciones_list = salida.get_asignaturas_secciones_list()
            for asignatura, total_secciones in asignaturas_secciones_list:
                salida_data=f"Actividad de salida: {salida.actividad} - (N.º de cuenta: {salida.numero_cuenta} - Fecha de salida: {salida.fecha_ingreso})"
                # Agregar la información a la lista
                asignaturas_secciones_data.append({
                    'asignatura': asignatura,
                    'total_secciones': total_secciones,
                    'salidadata' : salida_data
                })

        print("-----------blockcode----------------")
        for salida in salidas_activas:
            for seccion in salida.secciones.all():
                print(seccion.cantidad_alumnos())

        secciones_data = []  # Lista para almacenar la información de secciones y cantidad de alumnos

        for salida in salidas_activas:
            for seccion in salida.secciones.all():
                cantidad_alumnos = seccion.cantidad_alumnos()
                seccion_concatenada = f"{seccion.asignatura.sigla} - {seccion.nombre}" 
                seccion_asignaturanombre = f"{seccion.asignatura.nombre} - ( {seccion.asignatura.sigla} - {seccion.nombre} )" 
                print(cantidad_alumnos)
                # Agregar la información a la lista
                secciones_data.append({
                    'seccion': seccion_concatenada ,  # Supongamos que cada sección tiene un identificador único
                    'cantidad_alumnos': cantidad_alumnos,
                    'nombreAsig':seccion_asignaturanombre

                })

        
        print(secciones_data)



        print("------------------------------------------")



        # Obtener asignaturas con el conteo de secciones
        

        
        data = {
            'total_alumnos': total_alumnos,
            'total_salidas': total_salidas,
            'total_asignaturas': total_asignaturas,
            'total_secciones': total_seccionesv,
            'salidas_activas': salidas_activas,
            'asignaturas_secciones': asignaturas_secciones_data,
            'secciones': secciones_data 
        }
        return render(request, 'coordinador/home_coordinador.html', data)
    except:
        raise Http404
        
    

from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from .models import Asignatura, Seccion

def obtener_secciones(request):
    if request.method == 'GET':
        asignaturas = request.GET.getlist('asignaturas')  # Lista de IDs de asignaturas seleccionadas
        
        if not asignaturas:
            return JsonResponse([], safe=False)  # Retornar un JSON vacío si no hay asignaturas seleccionadas
        
        # Filtrar secciones relacionadas con las asignaturas seleccionadas
        secciones = Seccion.objects.filter(asignatura__id__in=asignaturas).select_related('asignatura')
        
        # Construir la respuesta JSON
        data = [
            {
                'id': seccion.id,
                'asignatura': seccion.asignatura.nombre,
                'seccion': seccion.nombre,
            }
            for seccion in secciones
        ]
        return JsonResponse(data, safe=False)

#usuarios --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------  listar usuario  -----------------------------------------------------

# def listar_usuario(request):
#     usuarios = UsersMetadata.objects.all().order_by('-id')
#     usuarios_data = []

#     for usuario in usuarios:
#         user_academy = UsersAcademy.objects.filter(user=usuario.user).first()
#         usuarios_data.append({
#             'usuario': usuario,
#             'user_academy': user_academy
#         })
#     page = request.GET.get('page', 1)

#     try:
#         paginator = Paginator(usuarios, 6)  # Cambio de cantidad a listar por usuario
#         usuarios = paginator.page(page)
#     except:
#         raise Http404

#     data = {
#         'usuarios': usuarios,
#         'paginator': paginator
#     }

#     return render(request, 'coordinador/usuarios/listar_usuarios.html', data)

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from core.models import UsersMetadata, UsersAcademy

def listar_usuario(request):
    usuarios_metadata = UsersMetadata.objects.all().order_by('-id')
    usuarios_data = []

    for usuario in usuarios_metadata:
        user_academy = UsersAcademy.objects.filter(user=usuario.user).first()
        usuarios_data.append({
            'usuario': usuario,
            'user': usuario.user,  # Ahora pasamos el usuario directamente
            'user_academy': user_academy
        })

    # Paginación
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(usuarios_data, 5)  # Cambio de cantidad a listar por usuario
        usuarios_paginados = paginator.page(page)
    except:
        raise Http404

    data = {
        'usuarios': usuarios_paginados,  # Ahora 'usuarios' tiene la estructura correcta
        'paginator': paginator
    }

    return render(request, 'coordinador/usuarios/listar_usuarios.html', data)


# ----------------------------------------  Lista de usuarios  -----------------------------------------------------


def lista_usuarios(request):
    # Obtener el valor de búsqueda del parámetro GET
    search_query = request.GET.get('search', '')

    # Filtrar los usuarios según el valor de búsqueda
    usuarios = UsersMetadata.objects.filter(
        Q(user__username__icontains=search_query) |
        Q(user__email__icontains=search_query) |
        Q(nombres__icontains=search_query) |
        Q(ap_paterno__icontains=search_query) |
        Q(ap_materno__icontains=search_query) |
        Q(rut__icontains=search_query) |
        Q(estado_civil__icontains=search_query) |
        Q(direccion__icontains=search_query) |
        Q(numero__icontains=search_query) |
        Q(celular__icontains=search_query) |
        Q(conctacto_sostenedor__icontains=search_query)
    ).distinct()

    # Obtener los filtros adicionales
    perfil_seleccionado = request.GET.get('perfil', '')
    sexo_seleccionado = request.GET.get('sexo', '')

    # Aplicar filtros adicionales si existen
    if perfil_seleccionado:
        usuarios = usuarios.filter(perfil=perfil_seleccionado)

    if sexo_seleccionado:
        usuarios = usuarios.filter(sexo=sexo_seleccionado)

    return render(request, 'coordinador/usuarios/listar_usuarios.html', {'usuarios': usuarios})


#----------------------------------------  Editar usuario  -----------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UsersMetadata, UsersAcademy
from .forms import UserEditForm, UsersMetadataForm, UsersAcademyForm

def editar_usuario(request, id):
    print("Entró a editar")
    print(id)

    # Obtener el usuario que se va a editar
    user = get_object_or_404(User, id=id)
    print(user)
    print("Pasó el user")

    # Obtener o crear las instancias de metadata y academia
    metadata, _ = UsersMetadata.objects.get_or_create(user=user)
    print(metadata)
    print("Pasó el metadata")
    
    academy, _ = UsersAcademy.objects.get_or_create(user=user)
    print(academy)
    print("Pasó la academia")

    if request.method == 'POST':
        # Crear las instancias de los formularios con los datos enviados por POST
        user_form = UserEditForm(request.POST, instance=user)
        metadata_form = UsersMetadataForm(request.POST, request.FILES, instance=metadata)
        academy_form = UsersAcademyForm(request.POST, instance=academy)

        # Validar los formularios
        if user_form.is_valid() and metadata_form.is_valid() and academy_form.is_valid():
            # Guardar el usuario
            user = user_form.save()

            # Guardar la metadata
            metadata = metadata_form.save(commit=False)
            metadata.user = user  # Asociar metadata al usuario
            metadata.username_field = user.username
            metadata.save()

            # Guardar la academia
            academy = academy_form.save(commit=False)
            academy.user = user  # Asociar academia al usuario
            academy.save()

            # Guardar las asignaturas seleccionadas (si existen)
            asignaturas_seleccionadas = request.POST.getlist('asignaturas_inscritas')
            academy.asignaturas_inscritas.set(asignaturas_seleccionadas)
            academy.save()

            messages.success(request, "Usuario actualizado correctamente!")
            return redirect('coordinador:home_coordinador')  # Redirigir después de guardar
        else:
            messages.error(request, "Errores en el formulario, por favor corrígelos.")

    else:
        # Si no es un POST, crear formularios con los datos del usuario
        user_form = UserEditForm(instance=user)
        metadata_form = UsersMetadataForm(instance=metadata)
        academy_form = UsersAcademyForm(instance=academy)

    return render(request, 'coordinador/usuarios/editar_usuario.html', {
        'user_form': user_form,
        'metadata_form': metadata_form,
        'academy_form': academy_form
    })


# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib import messages
# from .forms import UserCreationWithMetadataForm, UsersMetadataForm, UsersAcademyForm
# from .models import User  # Asegúrate de tener el modelo adecuado importado

# def editar_usuario(request, id):
#     # Obtener el usuario que se va a editar
#     user = get_object_or_404(User, id=id)

#     # Obtener las instancias actuales de metadata y academia
#     metadata = user.UsersMetadata  # Suponiendo que hay una relación uno a uno con metadata
#     academy = user.UsersAcademy  # Lo mismo para academia
    
#     if request.method == 'POST':
#         # Crear las instancias de los formularios con los datos enviados por POST
#         user_form = UserCreationWithMetadataForm(request.POST, instance=user)
#         metadata_form = UsersMetadataForm(request.POST, request.FILES, instance=metadata)
#         academy_form = UsersAcademyForm(request.POST, instance=academy)

#         # Validar los formularios
#         if user_form.is_valid() and metadata_form.is_valid() and academy_form.is_valid():
#             # Guardar el usuario
#             user = user_form.save()

#             # Guardar la metadata
#             metadata = metadata_form.save(commit=False)
#             metadata.user = user  # Asegurarse de que la metadata esté asociada al usuario
#             metadata.username_field = user.username
#             metadata.save()

#             # Guardar la academia
#             academy = academy_form.save(commit=False)
#             academy.user = user  # Asegurarse de que la academia esté asociada al usuario
#             academy.save()

#             # Guardar las asignaturas seleccionadas (si existen)
#             asignaturas_seleccionadas = request.POST.getlist('asignaturas_inscritas')
#             academy.asignaturas_inscritas.set(asignaturas_seleccionadas)
#             academy.save()

#             messages.success(request, "Usuario actualizado correctamente!")
#             return redirect('coordinador:home_coordinador')  # Redirigir después de guardar
#         else:
#             messages.error(request, "Errores en el formulario, por favor corrígelos.")
    
#     else:
#         # Si no es un POST, crear formularios con los datos del usuario
#         user_form = UserCreationWithMetadataForm(instance=user)
#         metadata_form = UsersMetadataForm(instance=metadata)
#         academy_form = UsersAcademyForm(instance=academy)

#     return render(request, 'coordinador/usuarios/editar_usuario.html', {
#         'user_form': user_form,
#         'metadata_form': metadata_form,
#         'academy_form': academy_form
#     })

# def eliminar_usuarios(request, id):
#     # Obtén la instancia del usuario que deseas eliminar
#     usuario = get_object_or_404(UsersMetadata, id=id)

#     if request.method == 'POST':
#         # Elimina el usuario
#         usuario.user.delete()
#         usuario.delete()
        
#         # Redirige a la página de lista de usuarios u otra página según tus necesidades
#         return redirect('gest-usuarios')

#     return render(request, 'ruta_de_la_plantilla_para_confirmar_eliminar.html', {'usuario': usuario})

    



   
        
       

     



      
      
  




# ----------------------------------------  Crear usuario  -----------------------------------------------------

def crear_usuario(request):
    if request.method == 'POST':
        # Crear las instancias de los formularios con los datos enviados por POST
        user_form = UserCreationWithMetadataForm(request.POST)
        metadata_form = UsersMetadataForm(request.POST, request.FILES)
        academy_form = UsersAcademyForm(request.POST)

        # Validar los formularios
        if user_form.is_valid() and metadata_form.is_valid() and academy_form.is_valid():
            # Guardar el usuario
            user = user_form.save()

            # Guardar la metadata
            metadata = metadata_form.save(commit=False)
            metadata.user = user
            metadata.username_field = user.username
            metadata.save()

            # Guardar la academia
            academy = academy_form.save(commit=False)
            academy.user = user
            academy.save()

            # Guardar las asignaturas seleccionadas (si existen)
            asignaturas_seleccionadas = request.POST.getlist('asignaturas_inscritas')
            academy.asignaturas_inscritas.set(asignaturas_seleccionadas)
            academy.save()

            messages.success(request, "Usuario agregado correctamente!")
            return redirect('coordinador:home_coordinador')  # Redirigir después de guardar
        else:
            messages.error(request, "Errores en el formulario, por favor corrígelos.")
    
    else:
        # Si no es un POST, crear formularios vacíos
        user_form = UserCreationWithMetadataForm()
        metadata_form = UsersMetadataForm()
        academy_form = UsersAcademyForm()

    return render(request, 'coordinador/usuarios/crear_usuario.html', {
        'user_form': user_form,
        'metadata_form': metadata_form,
        'academy_form': academy_form
    })





#crear grupo wsp ------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
@Coordinador_required
def crear_grupo_wsp(request):
    # Datos de ejemplo para los participantes
    participantes = ["56971678520","56994980015"]
    WHAPI_BEARER_TOKEN= "XzQPMnvGuJHKhaQczF8zkyGfsuFkYkMZ"

    url = "https://gate.whapi.cloud/groups"
    payload = {"participants": participantes, "subject": "Grupo de WhatsApp test"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {WHAPI_BEARER_TOKEN}"
    }

    try:
        print("Sending POST request to WHAPI")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("POST request successful")
        response_data = response.json()
        group_id = response_data.get('id', 'No ID found')
        print(f"Group ID: {group_id}")
        messages.success(request, f"Grupo de WhatsApp creado correctamente! ID: {group_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")
        messages.error(request, f"Error al crear el grupo de WhatsApp: {e}")

    return redirect('coordinador:home_coordinador')


#salidas ---------------------------------------------------------------------------------------------

@login_required
@Coordinador_required
def listar_salida(request):
    salidas = SalidaTerreno.objects.all().order_by('id')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(salidas, 6)  # Cambio de cantidad a listar por salida
        salidas = paginator.page(page)
    except:
        raise Http404

    # Agregar el conteo de alumnos inscritos en estado "ACTIVA"
    for salida in salidas:
        secciones = salida.secciones.all()
        salida.total_inscritos = Inscripcion.objects.filter(
            seccion__in=secciones,
            estado='ACTIVA'  # Filtro para solo incluir inscripciones activas
        ).count()

    data = {
        'salidas': salidas,
        'paginator': paginator
    }

    return render(request, 'coordinador/salidas/listar_salida.html', data)

# ----------------------------------------  Crear Salida  -----------------------------------------------------
@login_required
@Coordinador_required
def crear_salida(request):
        if request.method == 'POST':
            form = SalidaTerrenoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Salida de terreno creada correctamente!")
                return redirect('coordinador:listar_salida')
            else:
                messages.error(request, "Errores en el formulario, por favor corrígelos.")
        else:
            form = SalidaTerrenoForm()

        return render(request, 'coordinador/salidas/crear_salida.html', {
            'form': form
        })

# ----------------------------------------  Editar Salida  -----------------------------------------------------

@login_required
@Coordinador_required
def editar_salida(request, id):
    try:
        salida = SalidaTerreno.objects.get(id=id)
    except SalidaTerreno.DoesNotExist:
        messages.error(request, "La salida de terreno que intentas editar no existe.")
        return redirect('coordinador:listar_salida')
    
    if request.method == 'POST':
        form = SalidaTerrenoForm(request.POST, request.FILES, instance=salida)
        if form.is_valid():
            form.save()
            messages.success(request, "Salida de terreno actualizada correctamente!")
            return redirect('coordinador:listar_salida')
        else:
            messages.error(request, "Errores en el formulario, por favor corrígelos.")
    else:
        # Precarga de datos en el formulario
        initial_data = {
            'fecha_ingreso': salida.fecha_ingreso,
            'fecha_termino': salida.fecha_termino,
        }
        form = SalidaTerrenoForm(instance=salida, initial=initial_data)

    return render(request, 'coordinador/salidas/editar_salida.html', {
        'form': form,
        'salida': salida
    })

# ----------------------------------------  Eliminar Salida  -----------------------------------------------------
@login_required
@Coordinador_required
def eliminar_salida(request, id): #obtiene el id de la salida
    salida = get_object_or_404(SalidaTerreno, id=id) #obtiene la salida con el id obtenido
    salida.delete() #elimina la salida
    messages.success(request, f"La salida : {salida.actividad} - {salida.numero_cuenta}  ha sido eliminada correctamente.") #mensaje de confirmacion atravez de una variable que es leida por sweet alert y ejecutada 
    return redirect('coordinador:listar_salida') #redirecciona a la lista de salidas



#Asignaturas ------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------  Listar Asignaturas  -----------------------------------------------------

from django.shortcuts import render


def listar_asignatura(request):
    # Obtener todas las asignaturas ordenadas por semestre
    asignaturas = Asignatura.objects.select_related('coordinador__usersmetadata').order_by('semestre', 'nombre')

    # Agrupar asignaturas por semestre
    asignaturas_por_semestre = {}
    for semestre in range(1, 9):
        asignaturas_por_semestre[semestre] = asignaturas.filter(semestre=semestre)

    # Preparar el contexto
    contexto = {
        'asignaturas': asignaturas,  # Todas las asignaturas
        'asignaturas_por_semestre': asignaturas_por_semestre,  # Asignaturas por semestre
    }

    return render(request, 'coordinador/asignaturas/listar_asignatura.html', contexto)


# ----------------------------------------  Crear Asignatura  -----------------------------------------------------



    
@login_required
@Coordinador_required
def crear_asignatura(request):
        
        if request.method == 'POST':
            form = AsignaturaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Asignatura creada correctamente!")
                return redirect('coordinador:listar_asignatura')
            else:
                messages.error(request, "Errores en el formulario, por favor corrígelos.")
        else:
            form = AsignaturaForm()

        return render(request, 'coordinador/asignaturas/crear_asignatura.html', {
            'form': form
        })

@login_required
@Coordinador_required
def editar_asignatura(request, id):    
    try:
        asignatura = Asignatura.objects.get(id=id)
    except Asignatura.DoesNotExist:
        messages.error(request, "La asignatura que intentas editar no existe.")
        return redirect('coordinador:listar_asignatura')
    
    # Consulta las secciones asociadas a la asignatura
    secciones = Seccion.objects.filter(asignatura=asignatura).order_by('nombre')
    
    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignatura actualizada correctamente!")
            return redirect('coordinador:listar_asignatura')
        else:
            messages.error(request, "Errores en el formulario, por favor corrígelos.")
    else:
        form = AsignaturaForm(instance=asignatura)

    return render(request, 'coordinador/asignaturas/editar_asignatura.html', {
        'form': form,
        'asignatura': asignatura,
        'secciones': secciones  # Agregar secciones al contexto
    })



def eliminar_asignatura(request, id):
    return render(request, 'coordinador/asignaturas/eliminar_asignatura.html')


