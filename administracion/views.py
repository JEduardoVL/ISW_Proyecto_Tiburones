from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from usuarios.models import CustomUser
from .mixins import AdminRequiredMixin
from usuarios.forms import CustomUserCreationForm
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
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

# Alumnos
class AdministracionAlumnos(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/alumnos.html'
    # para ver las cuentas de los alumnos en tablas
def alumnos_view(request):
    alumnos = CustomUser.objects.filter(is_alumno=True)
    return render(request, 'Administracion/alumnos.html', {'alumnos': alumnos})

def get_alumno_data(request, id):
    """
    Vista para obtener los datos de un alumno específico.
    """
    if request.method == 'GET':
        try:
            alumno = CustomUser.objects.get(pk=id, is_alumno=True)
            data = {
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'correo_electronico': alumno.correo_electronico,
                'programa_academico': alumno.programa_academico,
                'estatus': alumno.estatus,
            }
            return JsonResponse({'status': 'success', 'data': data})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Alumno no encontrado'}, status=404)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_alumno_data(request, id):
    """
    Vista para actualizar los datos de un alumno específico.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alumno = CustomUser.objects.get(pk=id, is_alumno=True)
            alumno.nombre = data['nombre']
            alumno.apellido = data['apellido']
            alumno.correo_electronico = data['correo_electronico']
            alumno.programa_academico = data['programa_academico']
            alumno.estatus = data['estatus']
            alumno.save()
            return JsonResponse({'status': 'success', 'message': 'Datos actualizados correctamente'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Alumno no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["DELETE"])
def delete_alumno(request, id):
    """
    Vista para eliminar un alumno específico.
    """
    try:
        alumno = CustomUser.objects.get(pk=id, is_alumno=True)
        alumno.delete()
        return JsonResponse({'status': 'success', 'message': 'Alumno eliminado correctamente'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Alumno no encontrado'}, status=404)