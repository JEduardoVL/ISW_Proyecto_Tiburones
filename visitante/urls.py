# visitante/urls.py
from django.urls import path
from .views import VisitanteHomeView, VisitanteCbuscarView, VisitanteContactoView, VisitantePfrecuentesView, VisitanteBuscarView
from . import views

app_name = 'visitante'

urlpatterns = [
    path('home/', VisitanteHomeView.as_view(), name='home'),
    path('buscar/', VisitanteBuscarView.as_view(), name='buscar'), 
    path('como_buscar/', VisitanteCbuscarView.as_view(), name='como_buscar'),  
    path('preguntas_frecuentes/', VisitantePfrecuentesView.as_view(), name='preguntas_frecuentes'),  
    path('contactanos/', VisitanteContactoView.as_view(), name='contactanos'), 
    path('contact/', views.contact, name='contact'),
   # ... más patrones de URL ...
]

