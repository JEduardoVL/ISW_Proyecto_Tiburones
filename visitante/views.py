from django.views.generic import TemplateView

class VisitanteHomeView(TemplateView):
    template_name = 'visitante/home.html'

class VisitanteBuscarView(TemplateView): 
    template_name = 'visitante/buscar.html'

class VisitanteCbuscarView(TemplateView): 
    template_name = 'visitante/como_buscar.html'

class VisitantePfrecuentesView(TemplateView): 
    template_name = 'visitante/preguntas_frecuentes.html'

class VisitanteContactoView(TemplateView): 
    template_name = 'visitante/contactanos.html'