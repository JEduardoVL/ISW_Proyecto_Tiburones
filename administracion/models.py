from django.db import models

class FormaTitulacion(models.Model):
    convocatoria = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_limite_entrega = models.DateField()
    descripcion = models.TextField()
    requisitos = models.TextField()
    documentos_a_entregar = models.TextField()

    def __str__(self):
        return self.convocatoria
    
class Documento(models.Model):
    TIPO_CHOICES = (
        ('TT', 'Trabajo Terminal'),
        ('AR', 'Artículo'),
        ('TS', 'Tesis'),
        ('OT', 'Otro'),
    )
    
    nombre = models.CharField(max_length=255)
    resumen = models.TextField()
    palabras_clave = models.CharField(max_length=255)
    nombre_autor = models.CharField(max_length=100)
    sinodales = models.CharField(max_length=255)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    fecha_elaboracion = models.DateField()
    convocatoria_titulacion = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.nombre