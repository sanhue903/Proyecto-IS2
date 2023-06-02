from django.shortcuts import render
from django.shortcuts import redirect

from database.models import Bug, Proyecto, Avances, Programador, Imagen, ReporteBug
from django.contrib.auth.models import User

# Create your views here.

def index(request, bug_id):
    bug = Bug.objects.get(id_bug = bug_id)
    proyecto = Proyecto.objects.get(id_proyecto = bug.id_proyecto.id_proyecto)
    programador = bug.id_programador
    usuario_programador = User.objects.get(id = programador.user_id)
    avance = Avances.objects.order_by("-id_avance").filter(id_bug_id = bug_id)

    reporte = ReporteBug.objects.order_by("-id_reporte").filter(id_bug_id = bug_id)
    usuarios_reporte = User.objects.filter(id__in=reporte.values_list("id_usuario", flat=True))

    imagen = Imagen.objects.order_by("id_imagen").filter(id_reporte_id__in = reporte)

    context = {"bug": bug, 
               "proyecto": proyecto,
                "programador": usuario_programador, 
                "avance": avance, 
                "imagen":imagen, 
                "reporte": zip(reporte, usuarios_reporte)
                }
    
    return render(request, "bug_detail/index.html", context)