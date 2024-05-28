from django.db import models
from django.conf import settings 

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