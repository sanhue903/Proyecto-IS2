from django.shortcuts import render
from django.shortcuts import redirect

from database.models import Bug, Proyecto, Avances, Programador, Imagen, ReporteBug


# Create your views here.

def index(request, bug_id):
    bug = Bug.objects.get(id_bug = bug_id)
    proyecto = Proyecto.objects.get(id_proyecto = bug.id_proyecto)
    programador = Programador.objects.get(id_programador = bug.id_programador)
    avance = Avances.objects.order_by("id_avance").filter(id_bug_id = bug_id)

    reporte = ReporteBug.objects.order_by("id_reporte").filter(id_bug_id = bug_id)
    imagen = Imagen.objects.order_by("id_imagen").filter(id_reporte_id__in = reporte)


    context = {"bug": bug, "proyecto": proyecto, "programador": programador, "avance": avance, "imagen":imagen}
    return render(request, "bug_detail/index.html", context)