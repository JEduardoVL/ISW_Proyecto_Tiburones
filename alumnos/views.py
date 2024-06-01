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
from .models import Documento_alumno
from .subir_pre_alumno import upload_pdf
from administracion.models import Revisado

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProcesoTitulacion, DocumentoPropuestaAlumno
from .forms import DocumentoPropuestaAlumnoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

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

    def get(self, request, *args, **kwargs):
        documentos = Documento_alumno.objects.filter(usuario=request.user)
        if documentos.exists():
            documento = documentos.first()
            try:
                revisado = Revisado.objects.get(documento_alumno=documento)
            except Revisado.DoesNotExist:
                revisado = None
            return render(request, self.template_name, {'documento': documento, 'revisado': revisado})
        return render(request, self.template_name, {'documentos': None})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            nombre_documento = request.POST['nombre_documento']
            resumen = request.POST['resumen']
            nombre_autor = request.POST['nombre_autor']
            sinodales = request.POST['sinodales']
            tipo = request.POST['tipo']
            fecha_elaboracion = request.POST['fecha_elaboracion']
            convocatoria = request.POST['convocatoria']
            documento = request.FILES['documento']
            
            # Subir el documento a Google Drive y obtener la URL
            documento_url = upload_pdf(documento)
            
            documentos = Documento_alumno.objects.filter(usuario=request.user)
            if documentos.exists():
                # Actualizar el documento existente
                documento_alumno = documentos.first()
                documento_alumno.nombre_documento = nombre_documento
                documento_alumno.resumen = resumen
                documento_alumno.nombre_autor = nombre_autor
                documento_alumno.sinodales = sinodales
                documento_alumno.tipo = tipo
                documento_alumno.fecha_elaboracion = fecha_elaboracion
                documento_alumno.convocatoria = convocatoria
                documento_alumno.documento_url = documento_url
                documento_alumno.en_correccion = False
                documento_alumno.save()
            else:
                # Crear un nuevo documento
                nuevo_documento = Documento_alumno.objects.create(
                    usuario=request.user,
                    nombre_documento=nombre_documento,
                    resumen=resumen,
                    nombre_autor=nombre_autor,
                    sinodales=sinodales,
                    tipo=tipo,
                    fecha_elaboracion=fecha_elaboracion,
                    convocatoria=convocatoria,
                    documento_url=documento_url,
                    archivo_subido=True
                )
            return redirect('alumnos:subir_documento')

        return render(request, self.template_name)

    
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
        
        # Verificar el estado de 'enviado' y 'aceptado'
        if documento:
            if documento.enviado:
                proceso.enviar_propuesta = True
            if hasattr(documento, 'revisarpropuesta') and documento.revisarpropuesta.aceptado:
                proceso.resultado_propuesta = True
        
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
        return self.render_to_response({
            'form': form, 
            'documento': documento, 
            'revisar_propuesta': revisar_propuesta
        })

    def post(self, request, *args, **kwargs):
        documento = DocumentoPropuestaAlumno.objects.filter(alumno=request.user).first()
        form = DocumentoPropuestaAlumnoForm(request.POST, instance=documento) if documento else DocumentoPropuestaAlumnoForm(request.POST)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.alumno = request.user
            documento.enviado = True  # Actualizamos el campo 'enviado' a True
            documento.save()
            return redirect('alumnos:estatus_titulacion')
        revisar_propuesta = RevisarPropuesta.objects.filter(documento_alumno=documento).first() if documento else None
        return self.render_to_response({
            'form': form, 
            'documento': documento, 
            'revisar_propuesta': revisar_propuesta
        })

def documento_detalle(request, pk):
    documento = get_object_or_404(DocumentoPropuestaAlumno, pk=pk)
    return HttpResponse(f"Documento {documento.titulo} enviado con éxito.")
