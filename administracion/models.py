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

#Proceso de titulacion

class RevisarPropuesta(models.Model):
    documento_alumno = models.OneToOneField('alumnos.DocumentoPropuestaAlumno', on_delete=models.CASCADE)
    revisado = models.BooleanField(default=False)
    titulo_adecuado = models.BooleanField(null=True, blank=True)
    objetivos_planteados = models.BooleanField(null=True, blank=True)
    referencias_correctas = models.BooleanField(null=True, blank=True)
    errores_ortograficos = models.BooleanField(null=True, blank=True)
    normas_formato = models.BooleanField(null=True, blank=True)
    metodologia_descrita = models.BooleanField(null=True, blank=True)
    suficientes_referencias = models.BooleanField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    aceptado = models.BooleanField(default=False)

    def __str__(self):
        return f"Revisado: {self.revisado} - Documento: {self.documento_alumno.titulo}"

    def get_titulo_adecuado_display(self):
        return "Sí" if self.titulo_adecuado else "No"

    def get_objetivos_planteados_display(self):
        return "Sí" if self.objetivos_planteados else "No"

    def get_referencias_correctas_display(self):
        return "Sí" if self.referencias_correctas else "No"

    def get_errores_ortograficos_display(self):
        return "Sí" if self.errores_ortograficos else "No"

    def get_normas_formato_display(self):
        return "Sí" if self.normas_formato else "No"

    def get_metodologia_descrita_display(self):
        return "Sí" if self.metodologia_descrita else "No"

    def get_suficientes_referencias_display(self):
        return "Sí" if self.suficientes_referencias else "No"
    
