from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import ReporteBugForm, UsuarioForm
# Create your views here.

def home(request):
    return render(request,'home/index.html')

def home_buglist(request):
    return redirect('buglist:bugs_list')

def confirmacion_reporte(request):
    return render(request, 'home/confirmacion_reporte.html')

def reportar_bug(request):
    formBug = ReporteBugForm()
    formUsuario = UsuarioForm()
    print('definir forms')
    if request.method == 'POST':
        print('Entro al post')
        formBug = ReporteBugForm(request.POST)
        formUsuario == UsuarioForm(request.POST)
        if formBug.is_valid() and formUsuario.is_valid():
            print('son validos')
            reporteUsuario = formUsuario.save(commit=False)
            reporteUsuario.save()
            reporteBug = formBug.save(commit=False)
            reporteBug.save()
            print('antes del redirect')
            return redirect('home:confirmacion_reporte')
    else: 
        return render(request, 'home/reporte_bug.html', {'form': formBug})
    
