from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import ReporteBug, Bug
from database.models import ReporteBug, Bug, Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from datetime import datetime, timedelta
from django.utils import timezone
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from django.db.models import Count
import plotly.graph_objects as go
# Create your views here.


def home(request):

    if(request.user.is_authenticated == True):
        """ Inicio sesion """
        if(request.user.is_superuser == False):
            if(request.user.is_staff == True):
                """ Es programador """
                bugs_asignados = Bug.objects.filter(id_programador=request.user, estado="ASIGNADO" or "EN PROCESO")
                bugs_datas = []
                for bug in bugs_asignados:
                    Titulo = bugs_asignados["titulo"],
                    Proyecto = bugs_asignados["id_proyecto"],
                    bugs_datas.append({'Titulo': Titulo,'Proyecto': Proyecto})           
                df = pd.DataFrame(bugs_datas)
                if df.empty:
                    messages.warning(request, "No tienes errores asignados")
                    context = {
                        "bugs_asignados": bugs_asignados
                    }
                    return render(request,'home/start.html', context)
                else:
                    fig = px.bar(df, x='Titulo', y='Proyecto', width=1000)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='Segoe UI', color='white'))
                    gantt_plot = plot(fig, output_type='div')
                    context = {
                        "bugs_asignados": bugs_asignados,
                        "gantt_plot": gantt_plot
                        
                    }
                    
                    return render(request,'home/start.html', context)
                
            else:
                """ Es usuario registrado """
                usuario = Usuario.objects.get(id_user=request.user)
                reportes_usuario = ReporteBug.objects.filter(id_usuario = usuario)
                reportes_usario_id = reportes_usuario.values_list('id_reporte', flat=True)
                reportes_solucionados = Bug.objects.filter(id_bug__in=reportes_usario_id, estado="SOLUCIONADO").count()

                reportes_asignados= Bug.objects.filter(id_bug__in=reportes_usario_id, estado="ASIGNADO").count()
                reportes_enproceso= Bug.objects.filter(id_bug__in=reportes_usario_id, estado="EN PROCESO").count()
                context = {
                    "reportes_usuario": reportes_usuario,
                    "reportes_solucionados": reportes_solucionados,
                    "reportes_asignados": reportes_asignados,
                    "reportes_enproceso": reportes_enproceso
                }
                return render(request,'home/start.html',context)
        else:
            """ Es administrador """
            reportes = reportes = ReporteBug.objects.filter(fecha_reporte__gte=timezone.now()-timedelta(days=7)).values('fecha_reporte__date').annotate(cantidad_reportes=Count('id_reporte'))
            cant_reportes_pendientes = ReporteBug.objects.filter(estado="PENDIENTE").count()
            cant_reportes_asignados = ReporteBug.objects.filter(estado="ASIGNADO").count()
            cant_bugs_revision = Bug.objects.filter(estado="REVISION").count()
            reportes_data = []
            for reporte in reportes:
                fecha = reporte['fecha_reporte__date']
                cantidad = reporte['cantidad_reportes']
                reportes_data.append({'fecha': fecha, 'cantidad': cantidad})
                print(f"Fecha: {fecha}, Cantidad: {cantidad}")

            df = pd.DataFrame(reportes_data)
            if df.empty:
                messages.warning(request, "No hay reportes en los últimos 7 días")
                context = {
                'cant_reportes_pendientes': cant_reportes_pendientes,
                'cant_reportes_asignados': cant_reportes_asignados,
                'cant_bugs_revision': cant_bugs_revision,
                }
                return render(request,'home/start.html', context)
            fig = px.bar(df, x='fecha', y='cantidad', width=1000, color='cantidad')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='Segoe UI', color='white'))
            
            gantt_plot = plot(fig, output_type='div')
            context = {
                'plot_div': gantt_plot,
                'cant_reportes_pendientes': cant_reportes_pendientes,
                'cant_reportes_asignados': cant_reportes_asignados,
                'cant_bugs_revision': cant_bugs_revision,
            }
            return render(request,'home/start.html', context)
            
    else:
        listar_reportes = ReporteBug.objects.order_by("-fecha_reporte")[:5].select_related("id_proyecto")
        total_report = ReporteBug.objects.count()
        total_bug = Bug.objects.count()
        listar_bug = Bug.objects.order_by("-fecha_reporte")[:5].select_related("id_proyecto")


        context = {
            "listar_reportes": listar_reportes,
            "listar_bug": listar_bug,
            "total_report": total_report,
            "total_bug": total_bug
        }
        return render(request, 'home/start.html', context)
    
    

@login_required
def login(request):
    return redirect('home:principal')

def exit(request):
    logout(request)
    return redirect('home:principal')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() #guarda el usuario
            return redirect('home:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

