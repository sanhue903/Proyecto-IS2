from django.shortcuts import render
from django.shortcuts import redirect
from database.models import Bug, ReporteBug, Proyecto



# Create your views here.

def index(request):
    bug_list = Bug.objects.order_by("-fecha_reporte")
    report_list = ReporteBug.objects.order_by("-fecha_reporte")
    proyecto = Proyecto.objects.filter(id_proyecto__in=report_list.values_list("id_proyecto", flat=True))

    context = {"bug_list": bug_list, "report_list": zip(report_list, proyecto)}
    return render(request, "buglist/buglist.html", context)


def refresh(request):
    return redirect('buglist:index')