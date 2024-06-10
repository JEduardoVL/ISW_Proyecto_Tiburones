from django.views.generic import TemplateView
from .mixins import DocenteRequiredMixin
from django.http import JsonResponse
import json
from django.db.models import Q
# Importar vistas genéricas personalizadas
from django.views import View
from administracion.models import Documento
import spacy
from django.shortcuts import render

class DocenteHomeView(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/home.html'

class DocenteBuscar(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/buscar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ver_todo = self.request.GET.get('ver_todo')
        
        if ver_todo == '1':
            context['trabajos'] = Documento.objects.all()
        else:
            context['trabajos'] = Documento.objects.none()
        
        return context

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
    

class BuscarPorTipo_D(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/buscar_por_tipo_d.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.request.GET.get('tipo')
        if tipo:
            context['trabajos'] = Documento.objects.filter(tipo=tipo)
        else:
            context['trabajos'] = Documento.objects.none()
        return context

class BuscarPorPalabra_D(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/buscar_por_palabra_d.html'

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

class BuscarPorAño_D(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/buscar_por_año_d.html'

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

class BusquedaAvanzada_D(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/busqueda_avanzada_d.html'

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

class BuscarLenguajeNatural_D(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/busqueda_lenguaje_natural_d.html'

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
    
class DocenteVerTrabajo(DocenteRequiredMixin, TemplateView):
    template_name = 'docente/ver_trabajo_d.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documento_id = self.kwargs['pk']
        context['documento'] = Documento.objects.get(id=documento_id)
        return context