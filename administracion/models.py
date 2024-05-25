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
    url = models.URLField(blank=True, null=True)  # Hacer el campo opcional

    def __str__(self):
        return self.nombre

class Seminario(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField()
    presentador = models.CharField(max_length=100)
    temas = models.TextField()
    requisitos = models.TextField()
    creditos_academicos = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.titulo


class MaterialApoyo(models.Model):
    TIPO_CHOICES = [
        ('Guia', 'Guía'),
        ('Formato', 'Formato'),
        ('Ejemplo', 'Ejemplo'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=255) 
    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.nombre}"
