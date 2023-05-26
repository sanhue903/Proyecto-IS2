from django.shortcuts import render
from django.shortcuts import redirect

from database.models import Bug, Proyecto, Avances, Programador

# Create your views here.

def index(request, bug_id):
    bug = Bug.objects.get(id_bug = bug_id)
    proyecto = Proyecto.objects.get(id_proyecto = bug.id_proyecto.id_proyecto)
    programador = Programador.objects.get(id_programador = bug.id_programador.id_programador)
    avance = Avances.objects.order_by("id_avance").filter(id_bug_id = bug_id)


    context = {"bug": bug, "proyecto": proyecto, "programador": programador, "avance": avance}
    return render(request, "bug_detail/index.html", context)