def admin_info(request):
    if request.user.is_authenticated and hasattr(request.user, 'nombre'):
        return {
            'nombre_administrador': request.user.nombre,
            'apellido_administrador': request.user.apellido,
            'departamento_administrador': request.user.departamento_admin,
            'cargo_administrador': request.user.cargo,
            'correo_administrador': request.user.correo_electronico,
        }
    return {}