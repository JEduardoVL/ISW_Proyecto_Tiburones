from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin para requerir que el usuario sea administrador."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not getattr(request.user, 'is_administrador', False):  # Usar getattr para manejar si el atributo no existe
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('nombre_de_la_url_por_defecto')
        return super().dispatch(request, *args, **kwargs)
