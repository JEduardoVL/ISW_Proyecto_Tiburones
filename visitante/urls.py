# visitante/urls.py
from django.urls import path
from .views import VisitanteHomeView, VisitanteCbuscarView, VisitanteContactoView, VisitantePfrecuentesView, VisitanteBuscarView, VisitanteBuscarPorAño, VisitanteBuscarPorPalabra, VisitanteBuscarPorTipo, VisitanteBusquedaAvanzada, VisitanteVerTrabajo, VsitanteBuscarLenguajeNatural
from . import views

app_name = 'visitante'

urlpatterns = [
    path('home/', VisitanteHomeView.as_view(), name='home'),
    path('buscar/', VisitanteBuscarView.as_view(), name='buscar'), 
    path('como_buscar/', VisitanteCbuscarView.as_view(), name='como_buscar'),  
    path('preguntas_frecuentes/', VisitantePfrecuentesView.as_view(), name='preguntas_frecuentes'),  
    path('contactanos/', VisitanteContactoView.as_view(), name='contactanos'), 
    path('contact/', views.contact, name='contact'),
    path('buscar_por_año_visitante/', VisitanteBuscarPorAño.as_view(), name='buscar_por_año_visitante'), 
    path('buscar_por_palabra_visitante/', VisitanteBuscarPorPalabra.as_view(), name='buscar_por_palabra_visitante'),
    path('buscar_por_tipo_visitante/', VisitanteBuscarPorTipo.as_view(), name='buscar_por_tipo_visitante'),
    path('busqueda_avanzada_visitante/', VisitanteBusquedaAvanzada.as_view(), name='busqueda_avanzada_visitante'),
    path('busqueda_lenguaje_natural_visitante/', VsitanteBuscarLenguajeNatural.as_view(), name='busqueda_lenguaje_natural_visitante'),
    path('ver_trabajo_visitante/<int:pk>/', VisitanteVerTrabajo.as_view(), name='ver_trabajo_visitante'),
]

