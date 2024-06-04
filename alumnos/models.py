from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model
from administracion.models import RevisarPropuesta

    
# Proceso de titulacion
User = get_user_model()

class ProcesoTitulacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ver_info = models.IntegerField(default=0)
    enviar_propuesta = models.IntegerField(default=0)
    resultado_propuesta = models.IntegerField(default=0)
    desarrollo_proyecto = models.IntegerField(default=0)
    enviar_trabajo = models.IntegerField(default=0)

    def __str__(self):
        return f"Proceso de Titulación de {self.user.nombre} {self.user.apellido}"
    

class DocumentoPropuestaAlumno(models.Model):
    titulo = models.CharField(max_length=255)
    nombre_estudiante = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    nombre_directores = models.CharField(max_length=255)
    resumen = models.TextField()
    objetivos = models.TextField()
    metodologia = models.TextField()
    palabras_clave = models.CharField(max_length=255)
    referencias = models.TextField()
    convocatoria = models.CharField(max_length=4, default="2024")
    enviado = models.BooleanField(default=False)
    aceptado = models.BooleanField(default=False)
    sinodales = models.BooleanField(default=False)
    alumno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si el objeto se está creando por primera vez
            self.nombre_estudiante = self.alumno.nombre
            self.correo_electronico = self.alumno.correo_electronico
        super().save(*args, **kwargs)

        # Crear la instancia de RevisarPropuesta si no existe
        if not hasattr(self, 'revisarpropuesta'):
            RevisarPropuesta.objects.create(documento_alumno=self)

    def __str__(self):
        return self.titulo

class SinodalAsignado(models.Model):
    propuesta = models.ForeignKey('DocumentoPropuestaAlumno', on_delete=models.CASCADE)
    sinodal = models.ForeignKey('usuarios.CustomUser', on_delete=models.CASCADE)
    rol = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sinodal.nombre} - {self.rol}"