from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Campos generales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    
    # Campos específicos por tipo de usuario
    is_administrador = models.BooleanField(default=False)
    is_alumno = models.BooleanField(default=False)
    is_docente = models.BooleanField(default=False)
    
    # Alumno
    matricula = models.CharField(max_length=20, blank=True, null=True)
    programa_academico = models.CharField(max_length=100, blank=True, null=True)
    estatus = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('egresado', 'Egresado')], blank=True, null=True)
    
    # Docente
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    departamento_docente = models.CharField(max_length=100, blank=True, null=True)
    
    # Administrativo
    cargo = models.CharField(max_length=100, blank=True, null=True)
    departamento_admin = models.CharField(max_length=100, blank=True, null=True)

