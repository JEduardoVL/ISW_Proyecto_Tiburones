# docente/urls.py
from django.urls import path
from .views import DocenteHomeView, DocenteBuscar, DocentePreguntas, DocenteTrabajos, DocenteCambiarContrasena, DocenteInformacion
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_POST

app_name = 'docente'

urlpatterns = [
    path('home/', DocenteHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='docente-logout'),
    path('buscar/', DocenteBuscar.as_view(), name='buscar'),
    path('preguntas_frecuentes/', DocentePreguntas.as_view(), name='preguntas_frecuentes'),
    path('mis_trabajos/', DocenteTrabajos.as_view(), name='mis_trabajos'),
    # ... más patrones de URL ...
    path('informacion_docente/', DocenteInformacion.as_view(), name='informacion_docente'),
    path('cambiar_contrasena/', DocenteCambiarContrasena.as_view(), name='cambiar_contrasena'),
]
