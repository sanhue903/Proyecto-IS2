from django import forms
from database.models import ReporteBug, Usuario, Proyecto

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo_usuario']
        widgets = {
            'correo_usuario': forms.EmailInput(attrs={'placeholder': 'Introduzca su correo'})
        }

class ReporteBugForm(forms.ModelForm):
    class Meta:
        model = ReporteBug
        fields = ['reporte']
        widgets = {
            'reporte': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el problema aquí...'}),
        }

class ProyectoForm(forms.ModelForm):
    nombre_proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id_proyecto',
        label='Nombre del proyecto'
    )

    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto']

