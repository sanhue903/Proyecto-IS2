from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from bug_report.forms import ReporteBugForm, UsuarioForm, ProyectoForm, ImagenForm, TituloForm
from database.models import ReporteBug, Usuario, Proyecto, Imagen
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def reportar_bug(request):
    form_bug = ReporteBugForm()
    form_usuario = UsuarioForm()
    form_proyecto = ProyectoForm()
    form_imagen = ImagenForm()
    form_resumen = TituloForm()
    formulario_enviado = False

    if request.method == 'POST':
        form_bug = ReporteBugForm(request.POST)
        form_proyecto = ProyectoForm(request.POST)
        correo_usuario = request.POST.get('correo_usuario')
        form_imagen = ImagenForm(request.POST, request.FILES)
        form_resumen = TituloForm(request.POST)

        try:
            usuario = Usuario.objects.get(correo_usuario=correo_usuario)
        except Usuario.DoesNotExist:
            usuario = None

        id_proyecto = request.POST.get('nombre_proyecto')
        id_proyecto2 = Proyecto.objects.get(id_proyecto=id_proyecto)

        if form_bug.is_valid() and form_proyecto.is_valid() and form_resumen.is_valid():
            reporte_bug = form_bug.save(commit=False)
            reporte_bug.titulo = form_resumen.cleaned_data['titulo']

            if usuario:
                reporte_bug.correo_usuario = usuario
            else:
                form_usuario = UsuarioForm(request.POST)
                if form_usuario.is_valid():
                    usuario = form_usuario.save()
                    reporte_bug.correo_usuario = usuario
                else:
                    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario, 'form_proyecto': form_proyecto, 'form_imagen': form_imagen, 'form_resumen': form_resumen, 'formulario_enviado': formulario_enviado})
            
            reporte_bug.id_proyecto = id_proyecto2
            reporte_bug.save()

            for file in request.FILES.getlist('imagenes'):
                Imagen.objects.create(imagen=file, id_reporte=reporte_bug)

            formulario_enviado = True
            
            # Limpiar formularios después de enviar correctamente
            form_bug = ReporteBugForm()
            form_proyecto = ProyectoForm()
            form_imagen = ImagenForm()
            form_resumen = TituloForm()
            form_usuario = UsuarioForm()
        
        else:
            # Limpiar formularios
            form_bug = ReporteBugForm()
            form_proyecto = ProyectoForm()
            form_imagen = ImagenForm()
            form_resumen = TituloForm()
            form_usuario = UsuarioForm()
    else:
        form_bug = ReporteBugForm()
        form_usuario = UsuarioForm()
        form_proyecto = ProyectoForm()
        form_imagen = ImagenForm()
        form_resumen = TituloForm()

    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_usuario': form_usuario, 'form_proyecto': form_proyecto, 'form_imagen': form_imagen, 'form_resumen': form_resumen, 'formulario_enviado': formulario_enviado})


def confirmacion_reporte(request):
    return render(request, 'bug_report/confirmacion_reporte.html')