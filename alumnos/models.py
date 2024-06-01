from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model

class Documento_alumno(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre_documento = models.CharField(max_length=255)
    resumen = models.TextField()
    nombre_autor = models.CharField(max_length=255)
    sinodales = models.CharField(max_length=255)
    TIPOS_DOCUMENTO = [
        ('TT', 'Trabajo Terminal'),
        ('TE', 'Tesis'),
        ('OT', 'Otro'),
    ]
    tipo = models.CharField(max_length=2, choices=TIPOS_DOCUMENTO)
    fecha_elaboracion = models.DateField()
    convocatoria = models.CharField(max_length=255)
    documento_url = models.URLField(blank=True, null=True)
    archivo_subido = models.BooleanField(default=False)
    aceptado = models.BooleanField(default=False)
    en_correccion = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_documento
    
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
    nombre_estudiante = models.CharField(max_length=100)  # Se llenará automáticamente
    correo_electronico = models.EmailField()  # Se llenará automáticamente
    nombre_directores = models.CharField(max_length=255)
    resumen = models.TextField()
    objetivos = models.TextField()
    metodologia = models.TextField()
    palabras_clave = models.CharField(max_length=255)
    referencias = models.TextField()
    convocatoria = models.CharField(max_length=4, default="2024")
    enviado = models.BooleanField(default=False)
    aceptado = models.BooleanField(default=False)
    alumno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si el objeto se está creando por primera vez
            self.nombre_estudiante = self.alumno.nombre
            self.correo_electronico = self.alumno.correo_electronico
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo