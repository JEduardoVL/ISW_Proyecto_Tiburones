from django.views.generic import TemplateView
from .mixins import DocenteRequiredMixin

class DocenteHomeView(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/home.html'

class DocenteBuscar(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/buscar.html'

class DocenteTrabajos(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/mis_trabajos.html'

class DocentePreguntas(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/preguntas_frecuentes.html'