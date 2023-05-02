from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import ReporteBug, Bug
from database.models import ReporteBug, Bug
# Create your views here.


def home(request):
    listar_reportes = ReporteBug.objects.order_by("id_reporte")[:20]

    listar_bug = Bug.objects.order_by("id_bug")[:20]

    context = {
        "listar_reportes": listar_reportes,
        "listar_bug": listar_bug
    }
    return render(request, 'home/base.html', context)


# def home_inicio(request):
#     listar_reportes = ReporteBug.objects.order_by("id_reporte")[:20]

#     listar_bug = Bug.objects.order_by("id_bug")[:20]

#     context = {
#         "listar_reportes": listar_reportes,
#         "listar_bug": listar_bug
#     }
#     return render(request, "home/index.html", context)
