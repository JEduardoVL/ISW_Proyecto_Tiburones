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
    AdministracionAlumnos,
    alumnos_view,
    create_user,
    agregar_convocatoria,
    get_user_details,
    get_alumno_data,
    update_user,
    delete_user,
    AdministracionDocumentoFormView,  # Asegúrate de crear esta vista
    AdministracionDocumentoSuccessView,  # Vista de confirmación
    
)
from administracion import views
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LogoutView

app_name = 'administracion'  # Este es el namespace que debe coincidir con el utilizado en 'resolve_url'

urlpatterns = [
    path('home/', AdministracionHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='admin-logout'),

    path('informacion/', AdministracionInformacion.as_view(), name='informacion'),
    path('subir_documento/', AdministracionSubirDoc.as_view(), name='subir_documento'),
     path('titulacion/', AdministracionTitulacion.as_view(), name='titulacion'),
    path('seminarios/', AdministracionSeminarios.as_view(), name='seminarios'),
    path('convocatorias/', AdministracionConvocatorias.as_view(), name='convocatorias'),
    
     path('documento_form/', AdministracionDocumentoFormView.as_view(), name='documento_form'),  # Nueva ruta para el formulario de Documento
    path('documento_success/', AdministracionDocumentoSuccessView.as_view(), name='documento_success'),  # Nueva ruta para la vista de éxito

    # titulacion
    path('titulacion/registrar_formas_titulacion/', AdministracionTitulacionRegistrar.as_view(), name='registrar_formas_de_titulacion'),
    path('titulacion/calendario_titulacion/', AdministracionTitulacionCalendario.as_view(), name='calendario_titulacion'),
    path('convocatorias/agregar/', agregar_convocatoria, name='agregar_convocatoria'),

    path('titulacion/convocatorias_titulacion/', AdministracionTitulacionConvocatorias.as_view(), name='convocatorias_titulacion'),
    
    # cuentas
    path('cuentas/administrar_cuentas/', AdministracionAdminCuentas.as_view(), name='administrar_cuentas'),
    path('cuentas/crear_cuentas/', views.create_user, name='crear_cuentas'),
    path('cuentas/crear-usuario/', create_user, name='create_user'),  # Define la ruta y un nombre para la URL
    path('cuentas/get-user-details/<int:user_id>/', views.get_user_details, name='get-user-details'),
    path('cuentas/update-user/<int:user_id>/', views.update_user, name='update-user'),
    path('cuentas/update-user/<int:user_id>/', update_user, name='update-user'),
    path('cuentas/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # alumnos
    path('alumnos/', alumnos_view, name='alumnos'),
    path('alumnos/<int:id>/get_data/', views.get_alumno_data, name='get_alumno_data'),
    path('alumnos/<int:id>/update/', views.update_alumno_data, name='update_alumno_data'),
    path('alumnos/<int:id>/delete/', views.delete_alumno, name='delete_alumno'),

]
