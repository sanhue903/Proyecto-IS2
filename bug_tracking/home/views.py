from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import ReporteBug, Bug
from database.models import ReporteBug, Bug
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
# Create your views here.


def home(request):

    listar_reportes = ReporteBug.objects.order_by("fecha_reporte")[:5]
    total_report = ReporteBug.objects.count();
    total_bug = Bug.objects.count();
    listar_bug = Bug.objects.order_by("fecha_reporte")[:5]


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


# def home_inicio(request):
#     listar_reportes = ReporteBug.objects.order_by("id_reporte")[:20]

#     listar_bug = Bug.objects.order_by("id_bug")[:20]

#     context = {
#         "listar_reportes": listar_reportes,
#         "listar_bug": listar_bug
#     }
#     return render(request, "home/index.html", context)
