from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin para requerir que el usuario sea administrador."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si el usuario no está autenticado, redirige a la página de login.
            return self.handle_no_permission()
        if not request.user.is_administrador:
            # Si el usuario no es administrador, muestra un mensaje de error y redirige.
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('nombre_de_la_url_por_defecto')
        return super().dispatch(request, *args, **kwargs)
