from django.shortcuts import render, redirect
from django.contrib import messages
import plotly
from .models import ReporteBug, Bug
from database.models import ReporteBug, Bug, Usuario, Notificaciones
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from datetime import timedelta
from django.utils import timezone
import pandas as pd
import plotly.express as px
import plotly.offline as opy
from django.db.models import Count
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
                    gantt_plot = plotly(fig, output_type='div')
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
                notificaciones = Notificaciones.objects.filter(id_user=request.user)
                context = {
                    "reportes_usuario": reportes_usuario,
                    "reportes_solucionados": reportes_solucionados,
                    "reportes_asignados": reportes_asignados,
                    "reportes_enproceso": reportes_enproceso,
                    "notificaciones_usuario": notificaciones
                }
                return render(request, 'home/start.html', context)
        else:
            reportes_proyectos = ReporteBug.objects.filter(fecha_reporte__gte=timezone.now() - timedelta(days=7)).select_related('id_proyecto')
            proyectos = reportes_proyectos.values_list('id_proyecto__nombre_proyecto', flat=True).distinct()
            cant_reportes_pendientes = ReporteBug.objects.filter(estado="PENDIENTE").count()
            cant_reportes_asignados = ReporteBug.objects.filter(estado="ASIGNADO").count()
            cant_bugs_revision = Bug.objects.filter(estado="REVISION").count()
            reportes_data = []

            for proyecto in proyectos:
                reportes_proyecto = reportes_proyectos.filter(id_proyecto__nombre_proyecto=proyecto)
                cantidad_reportes = reportes_proyecto.count()
                reportes_data.append({'proyecto': proyecto, 'cantidad_reportes': cantidad_reportes})

            df = pd.DataFrame(reportes_data)

            if df.empty:
                messages.warning(request, "No hay reportes en los últimos 7 días")
                context = {
                    'cant_reportes_pendientes': cant_reportes_pendientes,
                    'cant_reportes_asignados': cant_reportes_asignados,
                    'cant_bugs_revision': cant_bugs_revision,
                }
                return render(request,'home/start.html', context)
            modo = obtenerDarkMode(request)
            if modo == 'dark':
                color_texto = '#707070'
                color_fondo = '#FFF'
            else:
                color_texto = '#ccc'
                color_fondo = '#242526'

            # Crear el gráfico de barras
            bar_fig = go.Figure(data=go.Bar(
                x=df['cantidad_reportes'],
                y=df['proyecto'],
                orientation='h',
            ))

            bar_fig.update_traces(
                marker_line_width=1.5,
                #opacity=0.6,
                showlegend=False,
            )
            bar_fig.update_layout(
                paper_bgcolor=color_fondo,
                plot_bgcolor=color_fondo,
                font=dict(family='Segoe UI', color=color_texto),
                yaxis=dict(
                    automargin=True,
                    tickmode='array',
                    ticktext=[proyecto for proyecto in df['proyecto']],
                    tickangle=0,
                    # Dar un espacio en pixeles entre proyectos y el eje y
                    ticksuffix='  ',
                ),
                dragmode=False,
                title='Reportes por proyecto en los últimos 7 días',
                yaxis_title='Proyecto',
                xaxis_title='Cantidad de reportes',

            )

            # Datos para el gráfico de torta
            cant_reportes_aprobados = ReporteBug.objects.filter(estado="APROBADO").count()
            cant_reportes_desaprobados = ReporteBug.objects.filter(estado="DESAPROBADO").count()
            cant_reportes_pendientes = ReporteBug.objects.filter(estado="PENDIENTE").count()
            labels = ['Aprobados', 'Desaprobados', 'Pendientes']
            values = [cant_reportes_aprobados, cant_reportes_desaprobados, cant_reportes_pendientes]

            # Crear el gráfico de torta
            pie_fig1 = go.Figure(data=go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                hoverinfo="label+percent",
                textinfo="value",
                textfont=dict(size=14),
                name='Estado de los reportes'
            ))

            # Personalizar el diseño del gráfico de torta
            pie_fig1.update_traces(
                hole=0.4,
                hoverinfo="label+percent",
                textinfo="value",
                textfont=dict(size=14)
            )
            pie_fig1.update_layout(
                paper_bgcolor=color_fondo,
                plot_bgcolor=color_fondo,
                font=dict(family='Segoe UI', color='white'),
                title='Estado de los reportes',
            )

            # Datos para el gráfico de torta de estados de los bugs
            cant_bugs_asignados = Bug.objects.filter(estado="ASIGNADO").count()
            cant_bugs_enproceso = Bug.objects.filter(estado="EN PROCESO").count()
            cant_bugs_solucionados = Bug.objects.filter(estado="SOLUCIONADO").count()
            labels_bugs = ['Asignados', 'En proceso', 'Solucionados']
            values_bugs = [cant_bugs_asignados, cant_bugs_enproceso, cant_bugs_solucionados]

            # Crear el segundo gráfico de torta
            pie_fig2 = go.Figure(data=go.Pie(
                labels=labels_bugs,
                values=values_bugs,
                hole=0.4,
                hoverinfo="label+percent",
                textinfo="value",
                textfont=dict(size=14),
                name='Estado de los bugs'
            ))
            # Personalizar el diseño del segundo gráfico de torta
            pie_fig2.update_traces(
                hole=0.4, 
                hoverinfo="label+percent", 
                textinfo="value", 
                textfont=dict(size=14)
            )
            pie_fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Segoe UI', color=color_texto),
                title='Estado de los bugs',
            )

            # Configurar los subplots
            fig = make_subplots(
                rows=1, 
                cols=2, 
                subplot_titles=(
                                "Estado de los reportes", 
                                "Estado de los bugs"
                                ), 
                specs=[[{"type": "pie"}, {"type": "pie"}]],
            )
            
            # Agregar el primer gráfico de torta a la subparcela (1, 2) con su propia leyenda
            fig.add_trace(pie_fig1.data[0], row=1, col=1,)

            # Agregar el segundo gráfico de torta a la subparcela (2, 2) con su propia leyenda
            fig.add_trace(pie_fig2.data[0], row=1, col=2,)

            fig.update_layout(
                paper_bgcolor=color_fondo,
                plot_bgcolor=color_fondo,
                font=dict(family='Segoe UI', color=color_texto),
                title_text="Reportes y bugs",
                height=400,
                width=1000,
                dragmode=False,

            )

            fig.update_layout(
                legend=dict(
                    yanchor="bottom",
                    y=0.1,
                    xanchor="center",
                    x=0.5
                )
            )

            bar_fig = bar_fig.to_html(full_html=False, default_height=300, default_width=1000, config={'displayModeBar': False})
            plot_div = fig.to_html(full_html=False, default_height=300, default_width=1000, config={'displayModeBar': False})

            context = {
                'cant_reportes_pendientes': cant_reportes_pendientes,
                'cant_reportes_asignados': cant_reportes_asignados,
                'cant_bugs_revision': cant_bugs_revision,
                'plot_div': plot_div,
                'bar_fig': bar_fig,
            }

            return render(request, 'home/start.html', context)

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
            form.save()  # guarda el usuario
            return redirect('home:login')

    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def check_username_availability(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            available = False
        except User.DoesNotExist:
            available = True
        return JsonResponse({'available': available})

def check_email_availability(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ## print('Email:', email)
        try:
            user = User.objects.get(email=email)
            available = False
        except User.DoesNotExist:
            available = True
        return JsonResponse({'available': available})
# def home_inicio(request):
#     listar_reportes = ReporteBug.objects.order_by("id_reporte")[:20]


def obtenerDarkMode(request):
    
    preferencia_color = request.headers.get('HTTP_ACCEPT')
    if preferencia_color and 'dark' in preferencia_color:
        return True
    else:
        return False
