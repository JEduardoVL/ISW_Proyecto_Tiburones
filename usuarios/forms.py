from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Campos generales
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    correo_electronico = forms.EmailField(required=True)
    
    # Añade los campos de radio con las nuevas opciones
    user_type = forms.ChoiceField(
        choices=[
            ('is_administrador', 'Administrador'), 
            ('is_alumno', 'Alumno'),
            ('is_docente', 'Docente')
        ],
        widget=forms.RadioSelect,
        required=True
    )
    
    matricula = forms.CharField(max_length=20, required=False)
    programa_academico = forms.CharField(max_length=100, required=False)
    estatus = forms.ChoiceField(choices=[('activo', 'Activo'), ('egresado', 'Egresado')], required=False)
    especialidad = forms.CharField(max_length=100, required=False)
    departamento_docente = forms.CharField(max_length=100, required=False)
    cargo = forms.CharField(max_length=100, required=False)
    departamento_admin = forms.CharField(max_length=100, required=False)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('nombre', 'apellido', 'correo_electronico', 'user_type', 
                                                  'matricula', 'programa_academico', 'estatus',
                                                  'especialidad', 'departamento_docente',
                                                  'cargo', 'departamento_admin',)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.apellido = self.cleaned_data['apellido']
        user.correo_electronico = self.cleaned_data['correo_electronico']
        user_type = self.cleaned_data['user_type']
        
        # Campos específicos por tipo de usuario
        if user_type == 'is_administrador':
            user.is_administrador = True
            user.cargo = self.cleaned_data['cargo']
            user.departamento_admin = self.cleaned_data['departamento_admin']
        elif user_type == 'is_alumno':
            user.is_alumno = True
            user.matricula = self.cleaned_data['matricula']
            user.programa_academico = self.cleaned_data['programa_academico']
            user.estatus = self.cleaned_data['estatus']
        elif user_type == 'is_docente':
            user.is_docente = True
            user.especialidad = self.cleaned_data['especialidad']
            user.departamento_docente = self.cleaned_data['departamento_docente']
        
        if commit:
            user.save()
        return user

