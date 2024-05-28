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
# Importar vistas genéricas personalizadas
from django.views import View
from .models import Documento_alumno
from .subir_pre_alumno import upload_pdf
from administracion.models import Revisado

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