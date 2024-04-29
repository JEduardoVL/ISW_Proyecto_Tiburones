from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from usuarios.models import CustomUser
from .mixins import AdminRequiredMixin
from usuarios.forms import CustomUserCreationForm
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse

# Todo lo necesario para la administracion de titulación
class AdministracionTitulacionRegistrar(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/registrar_formas_titulacion.html'
class AdministracionTitulacionCalendario(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/calendario_titulacion.html'
class AdministracionTitulacionConvocatorias(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/convocatorias_titulacion.html'

# Todo lo necesario para el manejo de las cuentas

class AdministracionAdminCuentas(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/cuentas/administrar_cuentas.html'


'''def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La cuenta de usuario ha sido creada con éxito.')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'administracion/cuentas/crear_cuentas.html', context)
'''

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'La cuenta de usuario ha sido creada con éxito.'
            return JsonResponse({'status': 'success', 'message': message})
        else:
            message = 'Por favor corrija los errores en el formulario.'
            return JsonResponse({'status': 'error', 'message': message})
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'administracion/cuentas/crear_cuentas.html', context)


# Alumnos
class AdministracionAlumnos(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/alumnos.html'
    # para ver las cuentas de los alumnos en tablas
def alumnos_view(request):
    alumnos = CustomUser.objects.filter(is_alumno=True)
    return render(request, 'Administracion/alumnos.html', {'alumnos': alumnos})


class AdministracionHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/home.html'

class AdministracionSubirDoc(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/subir_documento.html'

class AdministracionTitulacion(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/titulacion.html'


class AdministracionConvocatorias(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/convocatorias.html'

class AdministracionSeminarios(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/seminarios.html'

class AdministracionInformacion(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/informacion.html'

