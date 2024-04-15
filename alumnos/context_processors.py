def alumno_info(request):
    if request.user.is_authenticated and hasattr(request.user, 'nombre'):
        return {
            'nombre_alumno' : request.user.nombre,
            'apellido_alumno' :request.user.apellido,
            'boleta_alumno': request.user.matricula,
            'programa_academico': request.user.programa_academico,
            'estatus_alumno': request.user.estatus,
            'correo_alumno':request.user.correo_electronico,
        }
    return {}