# alumnos/views.py
from django.views.generic import TemplateView
from .mixins import AlumnoRequiredMixin

class AlumnosHomeView(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/home.html'

class AlumnosBuscar(AlumnoRequiredMixin,TemplateView):
    template_name = 'alumnos/buscar.html'

class AlumnosPreguntas(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/preguntas_frecuentes.html'

class AlumnosSubirDocumentos(AlumnoRequiredMixin,TemplateView):
    template_name = 'alumnos/subir_documento.html'

class AlumnosTitulacion(AlumnoRequiredMixin,TemplateView):
    template_name = 'alumnos/titulacion.html'
    
# Todo para la titulación
class AlumnosTitulacionCalendario(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/calendario_titulacion.html'
class AlumnosTitulacionConvocatoria(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/convocatorias_titulacion.html'
class AlumnosTitulacionForma(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/formas_titulacion.html'
class AlumnosTitulacionEstatus(AlumnoRequiredMixin, TemplateView):
    template_name = 'alumnos/titulacion/estatus_titulacion.html'