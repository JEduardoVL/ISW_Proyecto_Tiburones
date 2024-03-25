from django.contrib import admin
from django.urls import path, include
from usuarios.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),  # Incluye las URLs de la aplicación usuarios
    path('', CustomLoginView.as_view(), name='login'),  # El path vacío redirige al login
    path('administracion/', include('administracion.urls', namespace='administracion')),  # Incluye las URLs con el namespace
    path('alumnos/', include('alumnos.urls', namespace='alumnos')),
    path('visitante/', include(('visitante.urls', 'visitante'), namespace='visitante')),
    path('docente/', include('docente.urls', namespace='docente')),
    # ... cualquier otra ruta que necesites ...
]
