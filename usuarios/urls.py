from django.urls import path
from .views import SignUpView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # Asegúrate de que la URL de login esté incluida también
    # ...
]
