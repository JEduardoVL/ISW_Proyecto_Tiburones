from django import forms
from .models import Documento
from .models import Seminario
from .models import MaterialApoyo
from .models import RevisarPropuesta
from usuarios.models import CustomUser

class FileUploadForm(forms.Form):
    document = forms.FileField()

'''
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            'nombre', 'resumen', 'palabras_clave', 'nombre_autor', 'sinodales',
            'tipo', 'fecha_elaboracion', 'convocatoria_titulacion'
        ]
'''
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            'nombre', 'resumen', 'palabras_clave', 'nombre_autor', 'sinodales',
            'tipo', 'fecha_elaboracion', 'convocatoria_titulacion'
        ]
        widgets = {
            'fecha_elaboracion': forms.DateInput(attrs={'type': 'date'}),
        }
    url = forms.URLField(required=False, widget=forms.HiddenInput())
    
class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        kwargs['format'] = self.format
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            try:
                # Intentar convertir la cadena a un objeto de fecha
                value = datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                return value  # Devolver la cadena sin cambios si no se puede convertir
        return super().format_value(value)

class SeminarioForm(forms.ModelForm):
    class Meta:
        model = Seminario
        fields = ['titulo', 'fecha', 'hora', 'ubicacion', 'descripcion', 'presentador', 'temas', 'requisitos', 'creditos_academicos']
        widgets = {
            'fecha': DateInput(attrs={'placeholder': 'DD-MM-YYYY'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, '%d-%m-%Y').date()
            except ValueError:
                raise forms.ValidationError("Introduce una fecha válida en formato DD-MM-YYYY")
        return fecha

class MaterialApoyoForm(forms.ModelForm):
    class Meta:
        model = MaterialApoyo
        fields = ['tipo', 'nombre']
        
    archivo = forms.FileField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        # La URL será manejada por la vista después de la subida del archivo
        if commit:
            instance.save()
        return instance

#Proceso de titulacion

class RevisarPropuestaForm(forms.ModelForm):
    class Meta:
        model = RevisarPropuesta
        fields = [
            'titulo_adecuado', 'objetivos_planteados', 'referencias_correctas',
            'errores_ortograficos', 'normas_formato', 'metodologia_descrita',
            'suficientes_referencias', 'comentarios', 'aceptado'
        ]
        widgets = {
            'titulo_adecuado': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'objetivos_planteados': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'referencias_correctas': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'errores_ortograficos': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'normas_formato': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'metodologia_descrita': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'suficientes_referencias': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'aceptado': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
        }

class AsignarSinodalesForm(forms.Form):
    sinodal_1 = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_docente=True), label="Sinodal 1")
    sinodal_2 = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_docente=True), label="Sinodal 2")
    sinodal_3 = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_docente=True), label="Sinodal 3")
