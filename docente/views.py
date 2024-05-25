from django.views.generic import TemplateView
from .mixins import DocenteRequiredMixin
from django.http import JsonResponse
import json
from django.db.models import Q
# Importar vistas genéricas personalizadas
from django.views import View
from administracion.models import Documento

class DocenteHomeView(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/home.html'

class DocenteBuscar(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/buscar.html'

class DocenteTrabajos(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/mis_trabajos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_nombre = self.request.user.nombre
        docente_apellido = self.request.user.apellido
        
        # Filtrar documentos donde el docente aparece en sinodales o como autor
        documentos = Documento.objects.filter(
            Q(sinodales__icontains=docente_nombre) | 
            Q(sinodales__icontains=docente_apellido) |
            Q(nombre_autor__icontains=docente_nombre) |
            Q(nombre_autor__icontains=docente_apellido)
        ).distinct()
        
        context['documentos'] = documentos
        return context

class DocentePreguntas(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/preguntas_frecuentes.html'

class DocenteInformacion(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/informacion_docente.html'


class DocenteCambiarContrasena(View):
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