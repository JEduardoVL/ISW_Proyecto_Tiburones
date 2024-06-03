# administracion/urls.py

from django.urls import path
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    AdministracionHomeView,
    AdministracionSubirDoc,
    AdministracionTitulacion,
    AdministracionConvocatorias,
    AdministracionSeminarios,
    AdministracionInformacion,
    # titulacion
    AdministracionTitulacionConvocatorias,
    AdministracionTitulacionCalendario,
    AdministracionTitulacionRegistrar,
    # cuentas
    AdministracionAdminCuentas,
    
    # alumnos
    create_user,
    agregar_convocatoria,
    update_user,
    AdministracionCambiarContrasena,
    AdministracionEditarDatosGenerales,
    obtener_convocatoria,
    editar_convocatoria,
    eliminar_convocatoria,
    AdministracionAlumnos,
    EliminarMaterial,
    EditarMaterial,
    AdministracionDocumentosAlumnos,
    AdministracionDocumentosPrupuestaAlumnos,
    AdministracionDocumentosIndividualAlumnos,
    AdministracionAsignarSinodalesAlumnos,
    AdministracionVerDetallesPropuestaACS
)
from administracion import views
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LogoutView

app_name = 'administracion'  # Este es el namespace que debe coincidir con el utilizado en 'resolve_url'

urlpatterns = [
    path('home/', AdministracionHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='admin-logout'),
    
    # Ver información del administrador, edicion de datos y cambio de contraseña
    path('informacion/', AdministracionInformacion.as_view(), name='informacion'),
    path('editar_datos_generales/', AdministracionEditarDatosGenerales.as_view(), name='editar_datos_generales'),
    path('cambiar_contrasena/', AdministracionCambiarContrasena.as_view(), name='cambiar_contrasena'),

    path('subir_documento/', AdministracionSubirDoc.as_view(), name='subir_documento'),
     path('titulacion/', AdministracionTitulacion.as_view(), name='titulacion'),
    #path('seminarios/', AdministracionSeminarios.as_view(), name='seminarios'),
    path('convocatorias/', AdministracionConvocatorias.as_view(), name='convocatorias'),
    
    # path('documento_form/', AdministracionDocumentoFormView.as_view(), name='documento_form'),  # Nueva ruta para el formulario de Documento
    # path('documento_success/', AdministracionDocumentoSuccessView.as_view(), name='documento_success'),  # Nueva ruta para la vista de éxito

    path('seminarios/', views.seminarios, name='seminarios'),
    path('seminarios/eliminar/<int:id>/', views.eliminar_seminario, name='eliminar_seminario'),
    path('seminarios/editar/<int:id>/', views.editar_seminario, name='editar_seminario'),
    
    # titulacion
    path('titulacion/registrar_formas_titulacion/', AdministracionTitulacionRegistrar.as_view(), name='registrar_formas_de_titulacion'),
    path('titulacion/calendario_titulacion/', AdministracionTitulacionCalendario.as_view(), name='calendario_titulacion'),
    path('convocatorias/agregar/', agregar_convocatoria, name='agregar_convocatoria'),
    path('titulacion/convocatorias/obtener/<int:convocatoria_id>/', obtener_convocatoria, name='obtener_convocatoria'),
    path('titulacion/convocatorias/editar/<int:convocatoria_id>/', editar_convocatoria, name='editar_convocatoria'),
    path('titulacion/convocatorias/eliminar/<int:convocatoria_id>/', eliminar_convocatoria, name='eliminar_convocatoria'),
    path('titulacion/documentos_revision/', AdministracionDocumentosAlumnos.as_view(), name='documentos_revision'),


    path('titulacion/convocatorias_titulacion/', AdministracionTitulacionConvocatorias.as_view(), name='convocatorias_titulacion'),
    
    # cuentas
    path('cuentas/administrar_cuentas/', AdministracionAdminCuentas.as_view(), name='administrar_cuentas'),
    path('cuentas/crear_cuentas/', views.create_user, name='crear_cuentas'),
    path('cuentas/crear-usuario/', create_user, name='create_user'),  # Define la ruta y un nombre para la URL
    path('cuentas/get-user-details/<int:user_id>/', views.get_user_details, name='get-user-details'),
    path('cuentas/update-user/<int:user_id>/', views.update_user, name='update-user'),
    path('cuentas/update-user/<int:user_id>/', update_user, name='update-user'),
    path('cuentas/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('crear_usuario/', views.create_user, name='create_user'),
    
    # alumnos
    path('alumnos/', AdministracionAlumnos.as_view(), name='alumnos'),
    path('eliminar_material/<int:material_id>/', EliminarMaterial.as_view(), name='eliminar_material'),
    path('editar_material/', EditarMaterial.as_view(), name='editar_material'),

    # proceso de titulacion
    path('alumnos/revisar_propuestas_titulacion/', AdministracionDocumentosPrupuestaAlumnos.as_view(), name='revisar_propuestas_titulacion'),
    path('alumnos/individual_revisar_p/<int:pk>/', AdministracionDocumentosIndividualAlumnos.as_view(), name='individual_revisar_p'),
    path('alumnos/asignar_sinodales/<int:pk>/', AdministracionAsignarSinodalesAlumnos.as_view(), name='asignar_sinodales'),
    path('alumnos/ver_detalles/<int:pk>/', AdministracionVerDetallesPropuestaACS.as_view(), name='ver_detalles'),
] 
