# alumnos/urls.py
from django.urls import path
from .views import (
    AlumnosHomeView, 
    AlumnosBuscar, 
    AlumnosPreguntas, 
    AlumnosSubirDocumentos, 
    AlumnosTitulacion,
    # titulación
    AlumnosTitulacionCalendario,
    AlumnosTitulacionConvocatoria,
    AlumnosTitulacionForma,
    AlumnosTitulacionEstatus,
    AlumnosInformacion,
    AlumnosCambiarContrasena
)
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LogoutView

app_name = 'alumnos'

urlpatterns = [
    path('home/', AlumnosHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='alumno-logout'),
    path('buscar/', AlumnosBuscar.as_view(), name='buscar'),
    path('subir_documento/', AlumnosSubirDocumentos.as_view(), name='subir_documento'),
    path('preguntas_frecuentes/', AlumnosPreguntas.as_view(), name='preguntas_frecuentes'),
    path('titulacion/', AlumnosTitulacion.as_view(), name='titulacion'),

    path('informacion_alumnos/', AlumnosInformacion.as_view(), name='informacion_alumnos'),
    path('cambiar_contrasena/', AlumnosCambiarContrasena.as_view(), name='cambiar_contrasena'),
    # titulación
    path('titulacion/calendario_titulacion/', AlumnosTitulacionCalendario.as_view(), name='calendario_titulacion'),
    path('titulacion/convocatorias_titulacion/', AlumnosTitulacionConvocatoria.as_view(), name='convocatorias_titulacion'),
    path('titulacion/formas_titulacion/', AlumnosTitulacionForma.as_view(), name='formas_titulacion'),
    path('titulacion/estatus_titulacion/', AlumnosTitulacionEstatus.as_view(), name='estatus_titulacion'),
    
]

