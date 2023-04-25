from django import forms
from database.models import ReporteBug, Usuario

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

