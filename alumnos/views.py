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
from django.db.models import Q
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProcesoTitulacion, DocumentoPropuestaAlumno, SinodalAsignado
from .forms import DocumentoPropuestaAlumnoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import spacy
from administracion.utils import upload_pdf_admin
from administracion.forms import DocumentoForm
from django.urls import reverse_lazy

class AlumnosHomeView(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/home.html'

class BuscarPorTipo(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/buscar_por_tipo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.request.GET.get('tipo')
        if tipo:
            context['trabajos'] = Documento.objects.filter(tipo=tipo)
        else:
            context['trabajos'] = Documento.objects.none()
        return context

class BuscarPorPalabra(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/buscar_por_palabra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        palabra = self.request.GET.get('palabra')
        if palabra:
            context['trabajos'] = Documento.objects.filter(
                Q(nombre__icontains=palabra) | 
                Q(resumen__icontains=palabra) | 
                Q(palabras_clave__icontains=palabra)
            )
        else:
            context['trabajos'] = Documento.objects.none()
        return context

class BuscarPorAño(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/buscar_por_año.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        año = self.request.GET.get('año')
        if año:
            try:
                # Extraer solo el año
                año = int(año.split('-')[0])
                context['trabajos'] = Documento.objects.filter(fecha_elaboracion__year=año)
            except ValueError:
                context['trabajos'] = Documento.objects.none()
        else:
            context['trabajos'] = Documento.objects.none()
        return context

class BusquedaAvanzada(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/busqueda_avanzada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Q()

        palabra_b = self.request.GET.get('palabra')
        autor_b = self.request.GET.get('autor')
        documento_b = self.request.GET.get('documento')
        docente_b = self.request.GET.get('docente')
        sinodal_b = self.request.GET.get('sinodal')
        convocatoria_b = self.request.GET.get('convocatoria')
        tipo_b = self.request.GET.get('tipo')
        año_b = self.request.GET.get('año')

        if palabra_b:
            query &= Q(nombre__icontains=palabra_b) | Q(resumen__icontains=palabra_b) | Q(palabras_clave__icontains=palabra_b)
        if autor_b:
            query &= Q(nombre_autor__icontains=autor_b)
        if documento_b:
            query &= Q(nombre__icontains=documento_b)
        if docente_b:
            query &= Q(sinodales__icontains=docente_b)
        if sinodal_b:
            query &= Q(sinodales__icontains=sinodal_b)
        if convocatoria_b:
            query &= Q(convocatoria_titulacion__icontains=convocatoria_b)
        if tipo_b:
            query &= Q(tipo=tipo_b)
        if año_b:
            try:
                # Extraer solo el año
                año = int(año_b.split('-')[0])
                query &= Q(fecha_elaboracion__year=año)
            except ValueError:
                pass

        context['trabajos'] = Documento.objects.filter(query)
        return context

# Cargar el modelo de spaCy
pln = spacy.load('es_core_news_sm')

def procesar_texto(texto):
    doc = pln(texto)
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    return noun_chunks

class BuscarLenguajeNatural(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/busqueda_lenguaje_natural.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        trabajos = []
        if query:
            # Procesar el texto de búsqueda
            noun_chunks = procesar_texto(query)
            print(f"Noun chunks: {noun_chunks}")
            # Buscar en los documentos
            documentos = Documento.objects.all()
            for doc in documentos:
                for chunk in noun_chunks:
                    if chunk in doc.palabras_clave:
                        trabajos.append(doc)
                        break
            print(f"Documentos encontrados: {trabajos}")
        return render(request, self.template_name, {'trabajos': trabajos})
    
class AlumnosBuscar(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/buscar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ver_todo = self.request.GET.get('ver_todo')
        
        if ver_todo == '1':
            context['trabajos'] = Documento.objects.all()
        else:
            context['trabajos'] = Documento.objects.none()
        
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

class AlumnosProcesoTitulacionEnvDoc(FormView):
    template_name = 'alumnos/proceso_titulacion/envio_documento_p.html'
    form_class = DocumentoForm
    success_url = reverse_lazy('alumnos:proceso_titulacion_env_doc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['proceso_titulacion'] = ProcesoTitulacion.objects.get(user=user)
        return context

    def form_valid(self, form):
        user = self.request.user
        proceso_titulacion = ProcesoTitulacion.objects.get(user=user)
        
        if proceso_titulacion.enviar_trabajo == 1:
            return JsonResponse({'success': False, 'message': 'Documento ya enviado. No es necesario enviar otro.'})

        documento = self.request.FILES.get('documento')
        tipo = form.cleaned_data.get('tipo')

        folder_id = {
            'TT': '1PqOYnnBDJu_Jn0u2AMStKJPv4ZXZKnVy',
            'AR': '1UMp51OaLpqQKfhiBRIivF3pDTYZ5NIgk',
            'TS': '1SU5erynjS4MDMguKeWik_fZKLD5Ld_oipX',
            'OT': '1KJ1VLUd1dqCcS-zOUM_fZKLD5Ld_oipX'
        }.get(tipo, '1SU5erynjS4MDMguKeWik_faHNzYM90CB')

        if documento:
            try:
                file_url = upload_pdf_admin(documento, folder_id)
                form.instance.url = file_url
                form.save()

                # Actualizar el estado del proceso de titulación
                proceso_titulacion.enviar_trabajo = 1
                proceso_titulacion.save()
                
                success_message = "Archivo subido correctamente."
                return JsonResponse({'success': True, 'message': success_message})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': False, 'message': "Ocurrió un error al subir el archivo."})