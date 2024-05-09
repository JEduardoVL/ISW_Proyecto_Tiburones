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
from .models import FormaTitulacion
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string 
from django.views.generic.edit import FormView
from django import forms
from django.http import HttpResponseRedirect
from .utils import upload_pdf
from django.urls import reverse
from django.views.generic import FormView
from .forms import DocumentoForm, FileUploadForm
from .models import Documento
from smtplib import SMTPAuthenticationError

# Todo lo necesario para la administracion de titulación
class AdministracionTitulacionRegistrar(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/registrar_formas_titulacion.html'
class AdministracionTitulacionCalendario(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/calendario_titulacion.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['convocatorias'] = FormaTitulacion.objects.all()
        return context

@require_http_methods(["GET", "POST"])
def agregar_convocatoria(request):
    if request.method == 'POST':
        # Crear una instancia del modelo con los datos del formulario
        nueva_convocatoria = FormaTitulacion(
            convocatoria=request.POST['convocatoria'],
            fecha_inicio=request.POST['fecha_inicio'],
            fecha_limite_entrega=request.POST['fecha_limite_entrega'],
            descripcion=request.POST['descripcion'],
            requisitos=request.POST['requisitos'],
            documentos_a_entregar=request.POST['documentos_a_entregar'],
        )
        nueva_convocatoria.save()  # Guardar la instancia en la base de datos
        messages.success(request, 'Convocatoria agregada correctamente!')
        return redirect('administracion:calendario_titulacion')  # Redirigir a una URL específica después de guardar

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'administracion/titulacion/calendario_titulacion.html')

class AdministracionTitulacionConvocatorias(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/convocatorias_titulacion.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['convocatorias'] = FormaTitulacion.objects.all()
        return context

# Todo lo necesario para el manejo de las cuentas

class AdministracionAdminCuentas(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/cuentas/administrar_cuentas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recuperar todos los usuarios
        context['usuarios'] = CustomUser.objects.all()
        return context 
    

'''
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el nuevo usuario y recupéralo
            password = form.cleaned_data.get('password1')
            message = 'La cuenta de usuario ha sido creada con éxito.'
            
            # Renderizar la plantilla HTML con el email y la contraseña del usuario
            email_content = render_to_string('confirmacion_cuenta.html', {
                'email': user.correo_electronico,
                'password': password
            })
            
            # Enviar correo electrónico
            send_mail(
                subject='Confirmación de creación de cuenta',
                message=email_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.correo_electronico],
                fail_silently=False,
                html_message=email_content
            )
            
            return JsonResponse({'status': 'success', 'message': message})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'message': 'Por favor corrija los errores en el formulario.', 'errors': errors})
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'administracion/cuentas/crear_cuentas.html', context)
'''
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password1')
            message = 'La cuenta de usuario ha sido creada con éxito.'
            email_content = render_to_string('confirmacion_cuenta.html', {
                'email': user.correo_electronico,
                'password': password
            })
            try:
                send_mail(
                    subject='Confirmación de creación de cuenta',
                    message=email_content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.correo_electronico],
                    fail_silently=False,
                    html_message=email_content
                )
            except SMTPAuthenticationError:
                message += " Pero no se pudo enviar el correo de confirmación."

            return JsonResponse({'status': 'success', 'message': message})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'message': 'Por favor corrija los errores en el formulario.', 'errors': errors})
    else:
        form = CustomUserCreationForm()
        return render(request, 'administracion/cuentas/crear_cuentas.html', {'form': form})
    
class AdministracionHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/home.html'


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
    
# para cuentas generales
def get_user_details(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    if user is None:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    user_data = {
        'nombre': user.nombre,
        'apellido': user.apellido,
        'correo_electronico': user.correo_electronico,
        'is_alumno': user.is_alumno,
        'is_docente': user.is_docente,
        'is_administrador': user.is_administrador,
        'matricula': user.matricula,
        'programa_academico': user.programa_academico,
        'estatus': user.estatus,
        'especialidad': user.especialidad,
        'departamento_docente': user.departamento_docente,
        'cargo': user.cargo,
        'departamento_admin': user.departamento_admin,
    }
    return JsonResponse(user_data)
    
@require_http_methods(["POST"])
def update_user(request, user_id):
    try:
        user_data = json.loads(request.body)
        user = CustomUser.objects.get(id=user_id)

        # Actualizar campos generales
        user.nombre = user_data.get('nombre', user.nombre)
        user.apellido = user_data.get('apellido', user.apellido)
        user.correo_electronico = user_data.get('correo_electronico', user.correo_electronico)

        # Condiciones específicas para Alumno
        if user.is_alumno:
            user.matricula = user_data.get('matricula', user.matricula)
            user.programa_academico = user_data.get('programa_academico', user.programa_academico)
            user.estatus = user_data.get('estatus', user.estatus)

        # Condiciones específicas para Docente
        if user.is_docente:
            user.especialidad = user_data.get('especialidad', user.especialidad)
            user.departamento_docente = user_data.get('departamento_docente', user.departamento_docente)

        # Condiciones específicas para Administrador
        if user.is_administrador:
            user.cargo = user_data.get('cargo', user.cargo)
            user.departamento_admin = user_data.get('departamento_admin', user.departamento_admin)

        user.save()
        return JsonResponse({'message': 'Usuario actualizado con éxito'}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_administrador:
        return JsonResponse({'status': 'error', 'message': 'No autorizado'}, status=403)

    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'Usuario eliminado correctamente'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)
    


class FileUploadForm(forms.Form):
    document = forms.FileField()

class AdministracionSubirDoc(AdminRequiredMixin, FormView):
    template_name = 'administracion/subir_documento.html'
    form_class = FileUploadForm

    def form_valid(self, form):
        file = self.request.FILES['document']
        file_url = upload_pdf(file)

        # Guardar la URL en la sesión para su uso posterior
        self.request.session['uploaded_file_url'] = file_url

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administracion:documento_form')

class DocumentoFormView(AdminRequiredMixin, FormView):
    template_name = 'administracion/documento_form.html'
    form_class = DocumentoForm

    def form_valid(self, form):
        documento = form.save(commit=False)
        documento.url = self.request.session.get('uploaded_file_url')
        documento.save()

        # Limpiar la URL de la sesión
        del self.request.session['uploaded_file_url']

        return HttpResponseRedirect(reverse('administracion:home'))

class AdministracionDocumentoFormView(AdminRequiredMixin, FormView):
    template_name = 'administracion/documento_form.html'
    form_class = DocumentoForm

    def form_valid(self, form):
        documento = form.save(commit=False)
        documento.url = self.request.session.get('uploaded_file_url')
        documento.save()
        return HttpResponseRedirect(reverse('administracion:subir_documento'))

class AdministracionDocumentoSuccessView(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/documento_success.html'
