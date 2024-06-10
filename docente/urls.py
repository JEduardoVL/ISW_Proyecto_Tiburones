# docente/urls.py
from django.urls import path
from .views import DocenteHomeView, DocenteBuscar, DocentePreguntas, DocenteTrabajos, DocenteCambiarContrasena, DocenteInformacion, DocenteVerTrabajo, BuscarPorTipo_D, BuscarPorPalabra_D, BuscarPorAño_D, BusquedaAvanzada_D, BuscarLenguajeNatural_D
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_POST

app_name = 'docente'

urlpatterns = [
    path('home/', DocenteHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='docente-logout'),
    path('buscar/', DocenteBuscar.as_view(), name='buscar'),
    path('preguntas_frecuentes/', DocentePreguntas.as_view(), name='preguntas_frecuentes'),
    path('mis_trabajos/', DocenteTrabajos.as_view(), name='mis_trabajos'),
    path('informacion_docente/', DocenteInformacion.as_view(), name='informacion_docente'),
    path('cambiar_contrasena/', DocenteCambiarContrasena.as_view(), name='cambiar_contrasena'),
    path('ver_trabajo_d/<int:pk>/', DocenteVerTrabajo.as_view(), name='ver_trabajo_d'),
    path('buscar_por_tipo_d/', BuscarPorTipo_D.as_view(), name='buscar_por_tipo_d'),
    path('buscar_por_palabra_d/', BuscarPorPalabra_D.as_view(), name='buscar_por_palabra_d'),
    path('buscar_por_año_d/', BuscarPorAño_D.as_view(), name='buscar_por_año_d'),
    path('busqueda_avanzada_d/', BusquedaAvanzada_D.as_view(), name='busqueda_avanzada_d'),
    path('buscar-lenguaje-natural_d/', BuscarLenguajeNatural_D.as_view(), name='buscar_lenguaje_natural_d'),
]
