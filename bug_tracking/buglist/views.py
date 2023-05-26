from django.shortcuts import render
from django.shortcuts import redirect
from database.models import Bug, ReporteBug



# Create your views here.

def index(request):
    bug_list = Bug.objects.order_by("id_bug")[:20]
    report_list = ReporteBug.objects.order_by("id_reporte")[:20]
    context = {"bug_list": bug_list, "report_list": report_list}
    return render(request, "buglist/buglist.html", context)


def refresh(request):
    return redirect('buglist:index')