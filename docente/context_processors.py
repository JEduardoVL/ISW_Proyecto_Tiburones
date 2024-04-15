def docente_info(request):
    if request.user.is_authenticated and hasattr(request.user, 'nombre'):
        return {
            'nombre_docente': request.user.nombre,
            'apellido_docente': request.user.apellido,
            'especialidad_docente': request.user.especialidad,
            'departamento_docente': request.user.departamento_docente,
            'correo_docente': request.user.correo_electronico,
        }
    return {}