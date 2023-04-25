from django import forms
from database.models import ReporteBug, Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo_usuario']
        widgets = {
            'correo_usuario': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Introduzca su correo'})
        }


class ReporteBugForm(forms.ModelForm):
    class Meta:
        model = ReporteBug
        fields = ['reporte', 'correo_usuario']
        widgets = {
            'reporte': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el problema aquí...'}),
            'correo_usuario': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Introduzca su correo'})
        }