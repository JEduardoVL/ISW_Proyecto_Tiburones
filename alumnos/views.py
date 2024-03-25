# alumnos/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class AlumnosHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'alumnos/home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_alumno:
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('nombre_de_la_url_por_defecto')
        return super(AlumnosHomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AlumnosHomeView, self).get_context_data(**kwargs)
        context['nombre_alumno'] = self.request.user.nombre
        context['apellido_alumno'] = self.request.user.apellido
        context['boleta_alumno'] = self.request.user.matricula
        context['programa_academico'] = self.request.user.programa_academico
        context['estatus_alumno'] = self.request.user.estatus
        context['correo_alumno'] = self.request.user.correo_electronico
        return context