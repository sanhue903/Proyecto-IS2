from django import forms
from multiupload.fields import MultiFileField
from django.core.exceptions import ValidationError
from PIL import Image
from database.models import ReporteBug, Usuario, Proyecto, Imagen

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        
        fields = ['correo_usuario']
        widgets = {
            'correo_usuario': forms.EmailInput(attrs={
                'placeholder': 'Introduzca su correo',
                'rows': 2,
                })
        
        }
        
class ReporteBugForm(forms.ModelForm):
    imagenes = MultiFileField(min_num=0, max_num=4, max_file_size=1024*1024*4, required=False)

    def clean_imagenes(self):
        imagenes = self.cleaned_data.get('imagenes')
        for imagen in imagenes:
            try:
                img = Image.open(imagen)
                img.verify()
            except:
                raise forms.ValidationError('Solo se permiten archivos de imagen.')
            return imagenes

    class Meta:
        model = ReporteBug
        fields = ['reporte']
        widgets = {
            'reporte': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Describe el problema aquí...',
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