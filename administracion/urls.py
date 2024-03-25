# administracion/urls.py

from django.urls import path
from .views import AdministracionHomeView

app_name = 'administracion'  # Este es el namespace que debe coincidir con el utilizado en 'resolve_url'

urlpatterns = [
    path('home/', AdministracionHomeView.as_view(), name='home'),
    # ... otros patrones de URL ...
]
