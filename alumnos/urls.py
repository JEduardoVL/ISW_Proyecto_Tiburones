# alumnos/urls.py
from django.urls import path
from .views import AlumnosHomeView

app_name = 'alumnos'

urlpatterns = [
    path('home/', AlumnosHomeView.as_view(), name='home'),
    # ... más patrones de URL ...
]

