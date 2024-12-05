# import de librerias generales
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from core.decorators import Coordinador_required
# import de librerias crear usuarios
from .forms import UserCreationWithMetadataForm, UsersMetadataForm, UsersAcademyForm
# import de librerias listar salidas
from coordinador.models import SalidaTerreno




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
    salidas = SalidaTerreno.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(salidas, 6)#cambio de cantidad a listar por salida 
        salidas = paginator.page(page)
    except:
        raise Http404


    data = {
        'salidas': salidas,
        'paginator': paginator
    }

    return render(request, 'coordinador/salidas/listar_salida.html', data)