from django.shortcuts import render
from django.shortcuts import redirect
from database.models import Bug, ReporteBug, Proyecto



# Create your views here.

def index(request):
    bug_list = Bug.objects.order_by("-fecha_reporte")
    report_list = ReporteBug.objects.order_by("-fecha_reporte").select_related("id_proyecto")

    context = {"bug_list": bug_list, "report_list": report_list}
    return render(request, "buglist/buglist.html", context)


def refresh(request):
    return redirect('buglist:index')