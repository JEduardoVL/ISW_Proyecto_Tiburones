# docente/urls.py
from django.urls import path
from .views import DocenteHomeView
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_POST
from django.contrib.auth import logout

app_name = 'docente'

urlpatterns = [
    path('home/', DocenteHomeView.as_view(), name='home'),
    path('logout/', require_POST(LogoutView.as_view()), name='docente-logout'),
    # ... más patrones de URL ...
]
