from django.views.generic import TemplateView
from django.conf import settings
from .mixins import AdminRequiredMixin


# Todo lo necesario para la administracion de titulación
class AdministracionTitulacionRegistrar(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/registrar_formas_titulacion.html'
class AdministracionTitulacionCalendario(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/calendario_titulacion.html'
class AdministracionTitulacionConvocatorias(AdminRequiredMixin,TemplateView):
    template_name = 'administracion/titulacion/convocatorias_titulacion.html'

# Todo lo necesario para el manejo de las cuentas

class AdministracionAdminCuentas(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/cuentas/administrar_cuentas.html'
class AdministracionCreacionCuentas(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/cuentas/crear_cuentas.html'

# Alumnos
class AdministracionAlumnos(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/alumnos.html'


class AdministracionHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/home.html'

class AdministracionSubirDoc(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/subir_documento.html'

class AdministracionTitulacion(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/titulacion.html'


class AdministracionConvocatorias(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/convocatorias.html'

class AdministracionSeminarios(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/seminarios.html'

class AdministracionInformacion(AdminRequiredMixin, TemplateView):
    template_name = 'administracion/informacion.html'

