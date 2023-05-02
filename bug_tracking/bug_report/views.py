from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from bug_report.forms import ReporteBugForm, UsuarioForm
from database.models import ReporteBug, Usuario

# Create your views here.

def reportar_bug(request):
    form_bug = ReporteBugForm()
    form_usuario = UsuarioForm()
    if request.method == 'POST':
        form_bug = ReporteBugForm(request.POST)
        correo_usuario = request.POST.get('correo_usuario')
        try:
            usuario = Usuario.objects.get(correo_usuario=correo_usuario)
        except Usuario.DoesNotExist:
            usuario = None
        
        if form_bug.is_valid():
            reporte_bug = form_bug.save(commit=False)
            if usuario:
                reporte_bug.correo_usuario = usuario
            else:
                form_usuario = UsuarioForm(request.POST)
                if form_usuario.is_valid():
                    usuario = form_usuario.save()
                    reporte_bug.correo_usuario = usuario
                else:
                    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario})
            reporte_bug.save()
            return redirect('report:confirmacion_reporte')
    else:
        form_bug = ReporteBugForm()
        form_usuario = UsuarioForm()
    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario})

def confirmacion_reporte(request):
    return render(request, 'bug_report/confirmacion_reporte.html')