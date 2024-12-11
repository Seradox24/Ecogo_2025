# import de librerias generales
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from core.decorators import Coordinador_required
from core.models import Inscripcion
# import de librerias crear usuarios
from .forms import UserCreationWithMetadataForm, UsersMetadataForm, UsersAcademyForm
# import de librerias listar salidas
from coordinador.models import SalidaTerreno
from .forms import SalidaTerrenoForm
from django.shortcuts import get_object_or_404, redirect




#home coordinador -------------------------------------------------------------------------------------

@Coordinador_required
def home_coordinador(request):
    return render(request, 'coordinador/home_coordinador.html')


#usuarios ---------------------------------------------------------------------------------------------

@Coordinador_required
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

# ----------------------------------------  Listar Salida  -----------------------------------------------------
