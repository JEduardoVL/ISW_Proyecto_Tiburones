# Agrupar importaciones de django
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django import forms
from django.template.loader import render_to_string 
from django.http import JsonResponse, HttpResponse
import json

# Importar módulos específicos
from usuarios.models import CustomUser
from usuarios.forms import CustomUserCreationForm
from .mixins import AdminRequiredMixin
from .models import FormaTitulacion, Documento
from .forms import DocumentoForm, FileUploadForm
from .utils import upload_pdf
from .models import Seminario
from .forms import SeminarioForm

# Importar excepciones específicas
from smtplib import SMTPAuthenticationError

# Importar vistas genéricas personalizadas
from django.views import View

from .forms import MaterialApoyoForm
from .material_apoyo import upload_pdf
from .models import MaterialApoyo

# Todo lo necesario para la administracion de titulación
class AdministracionTitulacionRegistrar(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/registrar_formas_titulacion.html'


#*****************************************Calendario titulación****************************************************************

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

        # Enviar una respuesta JSON indicando éxito
        return JsonResponse({'success': True, 'message': 'Convocatoria agregada correctamente!'})

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'administracion/titulacion/calendario_titulacion.html')

@require_http_methods(["GET"])
def obtener_convocatoria(request, convocatoria_id):
    convocatoria = get_object_or_404(FormaTitulacion, id=convocatoria_id)
    data = {
        'convocatoria': convocatoria.convocatoria,
        'fecha_inicio': convocatoria.fecha_inicio,
        'fecha_limite_entrega': convocatoria.fecha_limite_entrega,
        'descripcion': convocatoria.descripcion,
        'requisitos': convocatoria.requisitos,
        'documentos_a_entregar': convocatoria.documentos_a_entregar,
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
def editar_convocatoria(request, convocatoria_id):
    convocatoria = get_object_or_404(FormaTitulacion, id=convocatoria_id)
    convocatoria.convocatoria = request.POST['convocatoria']
    convocatoria.fecha_inicio = request.POST['fecha_inicio']
    convocatoria.fecha_limite_entrega = request.POST['fecha_limite_entrega']
    convocatoria.descripcion = request.POST['descripcion']
    convocatoria.requisitos = request.POST['requisitos']
    convocatoria.documentos_a_entregar = request.POST['documentos_a_entregar']
    convocatoria.save()
    return JsonResponse({'success': True, 'message': 'Convocatoria actualizada correctamente!'})

@require_http_methods(["POST"])
def eliminar_convocatoria(request, convocatoria_id):
    convocatoria = get_object_or_404(FormaTitulacion, id=convocatoria_id)
    convocatoria.delete()
    return JsonResponse({'success': True, 'message': 'Convocatoria eliminada correctamente!'})

#*****************************************Canvocatorias titulación****************************************************************
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

class AdministracionEditarDatosGenerales(View):
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            user = request.user  # Asegurarse de que es el usuario actual o buscar por ID si necesario

            # Actualizar campos generales del administrador
            if hasattr(user, 'departamento_admin'):
                user.departamento_admin = user_data.get('departamento_admin', user.departamento_admin)
            if hasattr(user, 'cargo'):
                user.cargo = user_data.get('cargo', user.cargo)

            user.first_name = user_data.get('nombre', user.first_name)
            user.last_name = user_data.get('apellido', user.last_name)
            user.email = user_data.get('correo', user.email)

            user.save()
            return JsonResponse({'status': 'ok', 'message': 'Datos generales del administrador actualizados con éxito'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class AdministracionCambiarContrasena(View):
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')

        if not user.check_password(old_password):
            return JsonResponse({'status': 'error', 'message': 'Contraseña antigua incorrecta'}, status=403)

        if new_password:
            user.set_password(new_password)
        user.save()

        return JsonResponse({'status': 'ok', 'message': 'Contraseña cambiada con éxito'})
# Alumnos
class AdministracionAlumnos(AdminRequiredMixin, View):
    template_name = 'administracion/alumnos.html'

    def get(self, request):
        form = MaterialApoyoForm()
        materiales = MaterialApoyo.objects.all()
        return render(request, self.template_name, {'form': form, 'materiales': materiales})

    def post(self, request):
        form = MaterialApoyoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            try:
                url = upload_pdf(archivo)
                material_apoyo = form.save(commit=False)
                material_apoyo.url = url
                material_apoyo.save()
            finally:
                archivo.close() 

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class EliminarMaterial(View):
    def delete(self, request, material_id):
        try:
            material = MaterialApoyo.objects.get(id=material_id)
            material.delete()
            return HttpResponse(status=204)
        except MaterialApoyo.DoesNotExist:
            return JsonResponse({'error': 'Material no encontrado'}, status=404)

class EditarMaterial(View):
    def post(self, request):
        material_id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        archivo = request.FILES.get('archivo')

        try:
            material = MaterialApoyo.objects.get(id=material_id)
            material.nombre = nombre
            material.tipo = tipo

            if archivo:
                url = upload_pdf(archivo)
                material.url = url
                archivo.close()  

            material.save()
            return JsonResponse({'success': True})
        except MaterialApoyo.DoesNotExist:
            return JsonResponse({'error': 'Material no encontrado'}, status=404)
    
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

def seminarios(request):
    if request.method == 'POST':
        form = SeminarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administracion:seminarios')
        else:
            print("Errores en el formulario:", form.errors)  # Imprime los errores del formulario si no es válido
    else:
        form = SeminarioForm()

    seminarios = Seminario.objects.all()
    return render(request, 'administracion/seminarios.html', {'form': form, 'seminarios': seminarios})

def eliminar_seminario(request, id):
    seminario = get_object_or_404(Seminario, id=id)
    if request.method == 'POST':
        seminario.delete()
        return redirect('administracion:seminarios')
    return render(request, 'administracion/eliminar_seminario.html', {'seminario': seminario})

def editar_seminario(request, id):
    seminario = get_object_or_404(Seminario, id=id)
    if request.method == 'POST':
        form = SeminarioForm(request.POST, instance=seminario)
        if form.is_valid():
            form.save()
            return redirect('administracion:seminarios')
    else:
        form = SeminarioForm(instance=seminario)
    return render(request, 'administracion/editar_seminario.html', {'form': form, 'seminario': seminario})

