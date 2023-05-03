from django import forms
from database.models import ReporteBug, Usuario

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
    class Meta:
        model = ReporteBug
        fields = ['reporte']
        widgets = {
            'reporte': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Describe el problema aquí...',
                }),
        }
        

