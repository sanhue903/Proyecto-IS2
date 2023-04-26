from django.test import TestCase
from .models import *
# Create your tests here.

class DataBaseTest(TestCase):
    def setUp(self):
        #crear usuarios

        u1 = Usuario.objects.create("grupo7@is2.com")
        u1.save()

        #crear programadores

        p1 = Programador.objects.create(correo_programador="jvidal@udec.cl", nombre_programador="Javier Vidal")
        p2 = Programador.objects.create(correo_programador="jlopez@udec.cl", nombre_programador="Jorge Lopez")

        p1.save()
        p2.save()
        #crear proyectos

        proyecto1 = Proyecto.objects.create(nombre_proyecto="Infoda",)

        proyecto1.save()

        #crear cargos

        c1 = Cargo(
            programador = p1,
            proyecto = proyecto1,
        )

        c2 = Cargo(
            programador = p2,
            proyecto = proyecto1,
        )

        c1.save()
        c2.save()

        #crear reporteBug

        r1 = ReporteBug.objects.create(
            titulo= "no puedo entrar",
            reporte= "Usando Brave no puedo entrar al sistema",
            correo_usuario= u1,
        )

        r1.save()


        #crear Bug

        b1 = Bug.objects.create(
            descripcion = "no se puede entrar desde Brave",
            prioridad   = "media",
            estado      = "nuevo", 
            proyecto    = proyecto1,
            programador = p1,
        )

        b1.save()

        r1.bug = b1

        r1.save()
        
    def usuarioTest(self):
        u1 = Usuario.objects.get(correo_usuario="grupo7@is2.com")
        