from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import redirect, reverse
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
    return render(request, "home/index.html", context)


def home_buglist(request):
    return redirect('buglist:bugs_list')
