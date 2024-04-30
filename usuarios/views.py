'''from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.contrib import messages
from django.http import JsonResponse

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/signup.html'

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  

    def form_valid(self, form):
        # Aquí se maneja un login exitoso
        redirect_url = self.get_success_url()
        return JsonResponse({'redirect_url': redirect_url}, status=200)

    def form_invalid(self, form):
        # Aquí se maneja un login fallido
        return JsonResponse({'error': 'Usuario o contraseña incorrecta'}, status=400)

    def get_success_url(self):
        # Lógica para redirigir a diferentes usuarios a diferentes páginas
        if self.request.user.is_administrador:
            return resolve_url('administracion:home')
        elif self.request.user.is_alumno:
            return resolve_url('alumnos:home')
        elif self.request.user.is_docente:
            return resolve_url('docente:home')
        else:
            return resolve_url('url_por_defecto')'''

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.contrib import messages
from django.http import JsonResponse

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/signup.html'

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  

    def form_valid(self, form):
        # Aquí se maneja un login exitoso
        super().form_valid(form)  # Esto es necesario para establecer el login correctamente
        redirect_url = self.get_success_url()
        return JsonResponse({'redirect_url': redirect_url}, status=200)

    def form_invalid(self, form):
        # Aquí se maneja un login fallido
        return JsonResponse({'error': 'Usuario o contraseña incorrecta'}, status=400)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'is_administrador') and user.is_administrador:
            return resolve_url('administracion:home')
        elif hasattr(user, 'is_alumno') and user.is_alumno:
            return resolve_url('alumnos:home')
        elif hasattr(user, 'is_docente') and user.is_docente:
            return resolve_url('docente:home')
        else:
            return resolve_url('usuarios/login.html')
