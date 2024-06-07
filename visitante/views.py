from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from administracion.models import Documento
import spacy
from django.db.models import Q

class VisitanteHomeView(TemplateView):
    template_name = 'visitante/home.html'

class VisitanteVerTrabajo(TemplateView):
    template_name = 'visitante/ver_trabajo_visitante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documento_id = self.kwargs['pk']
        context['documento'] = Documento.objects.get(id=documento_id)
        return context
    
class VisitanteBuscarView(TemplateView): 
    template_name = 'visitante/buscar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ver_todo = self.request.GET.get('ver_todo')
        
        if ver_todo == '1':
            context['trabajos'] = Documento.objects.all()
        else:
            context['trabajos'] = Documento.objects.none()
        
        return context
    
class VisitanteBuscarPorTipo(TemplateView):
    template_name = 'visitante/buscar_por_tipo_visitante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.request.GET.get('tipo')
        if tipo:
            context['trabajos'] = Documento.objects.filter(tipo=tipo)
        else:
            context['trabajos'] = Documento.objects.none()
        return context

class VisitanteBuscarPorPalabra(TemplateView):
    template_name = 'visitante/buscar_por_palabra_visitante.html'

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

class VisitanteBuscarPorAño(TemplateView):
    template_name = 'visitante/buscar_por_año_visitante.html'

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

class VisitanteBusquedaAvanzada(TemplateView):
    template_name = 'visitante/busqueda_avanzada_visitante.html'

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

class VsitanteBuscarLenguajeNatural(TemplateView):
    template_name = 'visitante/busqueda_lenguaje_natural_visitante.html'

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
   
class VisitanteCbuscarView(TemplateView): 
    template_name = 'visitante/como_buscar.html'

class VisitantePfrecuentesView(TemplateView): 
    template_name = 'visitante/preguntas_frecuentes.html'

class VisitanteContactoView(TemplateView): 
    template_name = 'visitante/contactanos.html'

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        template = render_to_string('contacto.html', {
            'name': name,
            'email': email,
            'message': message
        })

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['aeneta.re@gmail.com']
        )

        email.fail_silently = False
        email.send()

        messages.success(request,' Correo enviado con exito.')
        return redirect('visitante:contactanos')
    
    # si no es la solicitus esperada
    return render(request, 'visitante:home.html')