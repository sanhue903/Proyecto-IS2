from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from bug_report.forms import ReporteBugForm, UsuarioForm, ProyectoForm
from database.models import ReporteBug, Usuario, Proyecto

# Create your views here.

def reportar_bug(request):
    form_bug = ReporteBugForm()
    form_usuario = UsuarioForm()
    form_proyecto = ProyectoForm()
    if request.method == 'POST':
        form_bug = ReporteBugForm(request.POST)
        form_proyecto = ProyectoForm(request.POST)
        correo_usuario = request.POST.get('correo_usuario')
        try:
            usuario = Usuario.objects.get(correo_usuario=correo_usuario)
        except Usuario.DoesNotExist:
            usuario = None
        id_proyecto = request.POST.get('nombre_proyecto')
        id_proyecto2 = Proyecto.objects.get(id_proyecto=id_proyecto)
        if form_bug.is_valid() and form_proyecto.is_valid():
            reporte_bug = form_bug.save(commit=False)
            # reporte_proyecto = form_proyecto.save(commit=False)
            if usuario:
                reporte_bug.correo_usuario = usuario
            else:
                form_usuario = UsuarioForm(request.POST)
                if form_usuario.is_valid():
                    usuario = form_usuario.save()
                    reporte_bug.correo_usuario = usuario
                else:
                    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario, 'form_proyecto': form_proyecto})
            
            # idProyecto = reporte_proyecto.save()
            reporte_bug.id_proyecto = id_proyecto2
            reporte_bug.save()
            return redirect('report:confirmacion_reporte')
    else:
        form_bug = ReporteBugForm()
        form_usuario = UsuarioForm()
        form_proyecto = ProyectoForm()
    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario, 'form_proyecto': form_proyecto})

def confirmacion_reporte(request):
    return render(request, 'bug_report/confirmacion_reporte.html')