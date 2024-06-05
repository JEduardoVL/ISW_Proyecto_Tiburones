# alumnos/views.py
from django.views.generic import TemplateView
from .mixins import AlumnoRequiredMixin
from django.shortcuts import render, redirect

from django.http import JsonResponse
import json
# Importamos el modelo
from administracion.models import FormaTitulacion
from administracion.models import MaterialApoyo
from administracion.models import Documento
from administracion.models import RevisarPropuesta
# Importar vistas genéricas personalizadas
from django.views import View
from .subir_pre_alumno import upload_pdf

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProcesoTitulacion, DocumentoPropuestaAlumno, SinodalAsignado
from .forms import DocumentoPropuestaAlumnoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class AlumnosHomeView(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/home.html'

class AlumnosBuscar(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/buscar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trabajos'] = Documento.objects.all()
        return context

class AlumnosVerTrabajo(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/ver_trabajo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documento_id = self.kwargs['pk']
        context['documento'] = Documento.objects.get(id=documento_id)
        return context


class AlumnosPreguntas(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/preguntas_frecuentes.html'

class AlumnosSubirDocumentos(TemplateView):
    template_name = 'alumnos/subir_documento.html'

    
class AlumnosTitulacion(AlumnoRequiredMixin,TemplateView):
    template_name = 'alumnos/titulacion.html'
    
# Todo para la titulación
class AlumnosTitulacionCalendario(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/calendario_titulacion.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['convocatorias'] = FormaTitulacion.objects.all()
        return context
    
class AlumnosTitulacionConvocatoria(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/convocatorias_titulacion.html'
class AlumnosTitulacionForma(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/formas_titulacion.html'


class AlumnosTitulacionEstatus(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/estatus_titulacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener o crear el proceso de titulación del usuario autenticado
        proceso, created = ProcesoTitulacion.objects.get_or_create(user=self.request.user)
        
        # Obtener el documento de propuesta del alumno
        documento = DocumentoPropuestaAlumno.objects.filter(alumno=self.request.user).first()
        
        # Verificar el estado de 'enviado', 'aceptado' y 'sinodales'
        if documento:
            if documento.enviado:
                proceso.enviar_propuesta = True
            if hasattr(documento, 'revisarpropuesta') and documento.revisarpropuesta.aceptado:
                proceso.resultado_propuesta = True
            if documento.sinodales:
                proceso.desarrollo_proyecto = True
        
        context['proceso'] = proceso
        return context


class AlumnosTitulacionMaterial(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/material_apoyo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guias'] = MaterialApoyo.objects.filter(tipo='Guía')
        context['formularios'] = MaterialApoyo.objects.filter(tipo='Formato')
        context['ejemplos'] = MaterialApoyo.objects.filter(tipo='Ejemplo')
        return context


class AlumnosInformacion(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/informacion_alumnos.html'


class AlumnosCambiarContrasena(View):
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
    

# -------------------Proceso de titulación-----------------------------------------

class AlumnosProcesoTitulacionInfo(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/proceso_titulacion/informacion.html'

class ActualizarVerInfo(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Obtener o crear el proceso de titulación del usuario autenticado
        proceso, created = ProcesoTitulacion.objects.get_or_create(user=request.user)
        proceso.ver_info = 1
        proceso.save()
        return redirect('alumnos:informacion')

class AlumnosProcesoTitulacionEnvPropuesta(TemplateView):
    template_name = 'alumnos/proceso_titulacion/enviar_propuesta.html'

    def get(self, request, *args, **kwargs):
        documento = DocumentoPropuestaAlumno.objects.filter(alumno=request.user).first()
        form = DocumentoPropuestaAlumnoForm(instance=documento) if documento else DocumentoPropuestaAlumnoForm()
        revisar_propuesta = RevisarPropuesta.objects.filter(documento_alumno=documento).first() if documento else None
        sinodales = SinodalAsignado.objects.filter(propuesta=documento) if documento and documento.sinodales else []
        return self.render_to_response({
            'form': form,
            'documento': documento,
            'revisar_propuesta': revisar_propuesta,
            'sinodales': sinodales
        })

    def post(self, request, *args, **kwargs):
        documento = DocumentoPropuestaAlumno.objects.filter(alumno=request.user).first()
        form = DocumentoPropuestaAlumnoForm(request.POST, instance=documento) if documento else DocumentoPropuestaAlumnoForm(request.POST)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.alumno = request.user
            documento.enviado = True  # Actualizamos el campo 'enviado' a True
            documento.save()

            # Enviar correo electrónico de confirmación
            correo_alumno = request.user.correo_electronico
            asunto = "Confirmación de envío de propuesta"
            mensaje = render_to_string('confirmacion_env_propuesta.html', {
                'nombre_alumno': request.user.nombre,
                'apellido_alumno': request.user.apellido,
                'documento': documento,
            })
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [correo_alumno],
                fail_silently=False,
                html_message=mensaje
            )

            return redirect('alumnos:estatus_titulacion')
        
        revisar_propuesta = RevisarPropuesta.objects.filter(documento_alumno=documento).first() if documento else None
        sinodales = SinodalAsignado.objects.filter(propuesta=documento) if documento and documento.sinodales else []
        return self.render_to_response({
            'form': form,
            'documento': documento,
            'revisar_propuesta': revisar_propuesta,
            'sinodales': sinodales
        })
    
def documento_detalle(request, pk):
    documento = get_object_or_404(DocumentoPropuestaAlumno, pk=pk)
    return HttpResponse(f"Documento {documento.titulo} enviado con éxito.")

class AlumnosProcesoTitulacionDesarrollo(TemplateView):
    template_name = 'alumnos/proceso_titulacion/desarrollo.html'