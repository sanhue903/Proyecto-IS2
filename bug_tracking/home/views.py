from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import ReporteBugForm, UsuarioForm
from database.models import ReporteBug, Usuario
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,'home/index.html')

def home_buglist(request):
    return redirect('buglist:bugs_list')

def confirmacion_reporte(request):
    return render(request, 'home/confirmacion_reporte.html')

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
                    return render(request, 'home/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario})
            reporte_bug.save()
            return redirect('home:confirmacion_reporte')
    else:
        form_bug = ReporteBugForm()
        form_usuario = UsuarioForm()
    return render(request, 'home/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario})





