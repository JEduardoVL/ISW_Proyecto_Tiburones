from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class AdministracionHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'administracion/home.html'


    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_administrador:
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('nombre_de_la_url_por_defecto')
        return super(AdministracionHomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdministracionHomeView, self).get_context_data(**kwargs)
        context['nombre_administrador'] = self.request.user.nombre
        context['apellido_administrador'] = self.request.user.apellido
        context['departamento_administrador'] = self.request.user.departamento_admin
        context['cargo_administrador'] = self.request.user.cargo
        context['correo_administrador'] = self.request.user.correo_electronico
        return context