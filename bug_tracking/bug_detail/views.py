from django.shortcuts import render
from django.shortcuts import redirect

from database.models import Bug, Proyecto, ReporteBug, Programador

# Create your views here.

def index(request, bug_id):
    bug = Bug.objects.get(id_bug = bug_id)
    proyecto = Proyecto.objects.get(id_proyecto = bug.id_proyecto.id_proyecto)
    programador = Programador.objects.get(id_programador = bug.id_programador.id_programador)
    reporte = ReporteBug.objects.order_by("id_reporte").filter(id_bug_id = bug_id)[:20]


    context = {"bug": bug, "proyecto": proyecto, "programador": programador, "reporte": reporte}
    return render(request, "bug_detail/index.html", context)