from django import forms
from .models import Documento

class FileUploadForm(forms.Form):
    document = forms.FileField()

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            'nombre', 'resumen', 'palabras_clave', 'nombre_autor', 'sinodales',
            'tipo', 'fecha_elaboracion', 'convocatoria_titulacion'
        ]
