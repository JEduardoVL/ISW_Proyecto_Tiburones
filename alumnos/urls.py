# alumnos/urls.py
from django import views
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
    AlumnosCambiarContrasena,
    AlumnosTitulacionMaterial,
    AlumnosVerTrabajo,

    AlumnosProcesoTitulacionInfo,
    ActualizarVerInfo,
    AlumnosProcesoTitulacionEnvPropuesta,
    documento_detalle,
    AlumnosProcesoTitulacionDesarrollo,
    BuscarPorAño,
    BuscarPorPalabra,
    BuscarPorTipo,
    BusquedaAvanzada,
    BuscarLenguajeNatural,
    AlumnosProcesoTitulacionEnvDoc
)
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LogoutView

app_name = 'alumnos'

urlpatterns = [
    path('home/', AlumnosHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='alumno-logout'),
    path('buscar/', AlumnosBuscar.as_view(), name='buscar'),
     path('ver_trabajo/<int:pk>/', AlumnosVerTrabajo.as_view(), name='ver_trabajo'),
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
    path('titulacion/material_apoyo/', AlumnosTitulacionMaterial.as_view(), name='material_apoyo'),

    # Porceso de titulacion
    path('proceso_titulacion/informacion/', AlumnosProcesoTitulacionInfo.as_view(), name='informacion'),
    path('proceso_titulacion/actualizar_ver_info/', ActualizarVerInfo.as_view(), name='actualizar_ver_info'),
    path('proceso_titulacion/enviar_propuesta/', AlumnosProcesoTitulacionEnvPropuesta.as_view(), name='enviar_propuesta'),
    path('documento/<int:pk>/', documento_detalle, name='documento_detalle'),
    path('proceso_titulacion/desarrollo/', AlumnosProcesoTitulacionDesarrollo.as_view(), name='desarrollo'),
    path('proceso_titulacion/envio_documento_p',AlumnosProcesoTitulacionEnvDoc.as_view(), name='envio_documento_p'),

    path('buscar_por_tipo/', BuscarPorTipo.as_view(), name='buscar_por_tipo'),
    path('buscar_por_palabra/', BuscarPorPalabra.as_view(), name='buscar_por_palabra'),
    path('buscar_por_año/', BuscarPorAño.as_view(), name='buscar_por_año'),
    path('busqueda_avanzada/', BusquedaAvanzada.as_view(), name='busqueda_avanzada'),
    path('buscar-lenguaje-natural/', BuscarLenguajeNatural.as_view(), name='buscar_lenguaje_natural'),
]

