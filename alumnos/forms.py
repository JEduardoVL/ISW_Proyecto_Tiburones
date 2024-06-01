# alumnos/forms.py
from django import forms
from .models import DocumentoPropuestaAlumno

class DocumentoPropuestaAlumnoForm(forms.ModelForm):
    class Meta:
        model = DocumentoPropuestaAlumno
        fields = ['titulo', 'nombre_directores', 'resumen', 'objetivos', 'metodologia', 'palabras_clave', 'referencias']
