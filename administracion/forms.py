from django import forms
from .models import Documento
from .models import Seminario
from .models import MaterialApoyo
from .models import Revisado

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
    
class RevisadoForm(forms.ModelForm):
    class Meta:
        model = Revisado
        fields = [
            'titulo_adecuado',
            'objetivos_cumplidos',
            'referencias_correctas',
            'errores_ortograficos',
            'estructura_clara',
            'contenido_coherente',
            'normas_formato',
            'metodologia_descrita',
            'resultados_presentados',
            'discusion_adecuada',
            'conclusiones_pertinentes',
            'suficientes_referencias',
            'introduccion_contextualiza',
            'graficos_tablas_adecuados',
            'resumen_claro_conciso',
            'comentarios'
        ]
        widgets = {
            'titulo_adecuado': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'objetivos_cumplidos': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'referencias_correctas': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'errores_ortograficos': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'estructura_clara': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'contenido_coherente': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'normas_formato': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'metodologia_descrita': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'resultados_presentados': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'discusion_adecuada': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'conclusiones_pertinentes': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'suficientes_referencias': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'introduccion_contextualiza': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'graficos_tablas_adecuados': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'resumen_claro_conciso': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
            'comentarios': forms.Textarea(attrs={'rows': 4}),
        }