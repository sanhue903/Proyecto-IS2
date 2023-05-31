from django import forms
from multiupload.fields import MultiFileField
from django.core.exceptions import ValidationError
from PIL import Image
from database.models import ReporteBug, Usuario, Proyecto, Imagen
from django.core.validators import FileExtensionValidator

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        
        fields = ['user']
        widgets = {
            'user.email': forms.EmailInput(attrs={
                'placeholder': 'Introduzca su correo',
                'rows': 2,
                })
        
        }
        
class ReporteBugForm(forms.ModelForm):

    class Meta:
        model = ReporteBug
        fields = ['reporte']
        widgets = {
            'reporte': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Describe el problema aquí...',
                'style':'resize:none;',
                }),
        }       

class ProyectoForm(forms.ModelForm):
    nombre_proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        empty_label='---',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id_proyecto',
        label='Nombre del proyecto',
        initial=None,
    )

    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto']


class TituloForm(forms.ModelForm):
    class Meta:
        model = ReporteBug
        fields = ['titulo']
        widgets = {
            'titulo': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'Resumen del problema ...',
                'style':'resize:none;',
                }),
        }

class ImagenForm(forms.ModelForm):
    imagenes = forms.FileField(widget=forms.FileInput(attrs={
        'multiple': True,
        'class': 'form-control-file',
        'validators': [FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])],
    }), required=False)

    class Meta:
        model = Imagen
        fields = ['imagenes']
