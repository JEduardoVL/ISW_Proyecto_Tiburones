from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class DocenteHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'docente/home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_docente:
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('nombre_de_la_url_por_defecto')
        return super(DocenteHomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocenteHomeView, self).get_context_data(**kwargs)
        context['nombre_docente'] = self.request.user.nombre
        context['apellido_docente'] = self.request.user.apellido
        context['especialidad_docente'] = self.request.user.especialidad
        context['departamento_docente'] = self.request.user.departamento_docente
        context['correo_docente'] = self.request.user.correo_electronico
        return context