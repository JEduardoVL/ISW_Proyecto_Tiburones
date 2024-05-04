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