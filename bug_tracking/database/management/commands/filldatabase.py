from database.models import *
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.wsgi import get_wsgi_application
from django.core.management.base import BaseCommand, CommandError

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bug_tracking.settings")
application = get_wsgi_application()


from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.filter(name='empleados').delete()


        programadores_group = Group(name='empleados')
        programadores_group.save()

        # añadir permisos para editar objetos del modelo Avances
        avances_type = ContentType.objects.get_for_model(Avances)

        add_permission = Permission.objects.get(
            codename="add_avances", content_type=avances_type)
        change_permission = Permission.objects.get(
            codename="change_avances", content_type=avances_type)
        delete_permission = Permission.objects.get(
            codename="delete_avances", content_type=avances_type)

        programadores_group.permissions.add(
            add_permission, change_permission, delete_permission)

        programadores_group.save()
        # anadir permiso de reasignacion

        reasignacion_type = ContentType.objects.get_for_model(Reasignacion)
        add_permission_reasignacion = Permission.objects.get(
            codename="add_reasignacion", content_type=reasignacion_type)
        view_permission = Permission.objects.get(
            codename="view_reasignacion", content_type=reasignacion_type)
        programadores_group.permissions.add(
            add_permission_reasignacion, view_permission)
        programadores_group.save()

        # Añadir permiso para ver objetos del modelo ReporteBug
        reportebug_type = ContentType.objects.get_for_model(ReporteBug)
        view_permission = Permission.objects.get(
            codename="view_reportebug", content_type=reportebug_type)

        programadores_group.permissions.add(view_permission)

        programadores_group.save()

        # Añadir permiso para ver objetos del modelo Bug
        bug_type = ContentType.objects.get_for_model(Bug)
        view_permission = Permission.objects.get(
            codename="view_bug", content_type=bug_type)

        programadores_group.permissions.add(view_permission)

        programadores_group.save()

        # crear grupo usuario
        Group.objects.filter(name='clientes').delete()

        usuarios_group = Group(name='clientes')
        usuarios_group.save()
        # añadir permiso reportebug
        reportebug_type = ContentType.objects.get_for_model(ReporteBug)
        add_permission = Permission.objects.get(
            codename="add_reportebug", content_type=reportebug_type)
        usuarios_group.permissions.add(add_permission)
        usuarios_group.save()
        
        programadores_group = Group(name='empleados')
        programadores_group.save()

        #añadir permisos para editar objetos del modelo Avances
        avances_type = ContentType.objects.get_for_model(Avances)

        add_permission = Permission.objects.get(codename="add_avances", content_type=avances_type)
        change_permission = Permission.objects.get(codename="change_avances", content_type=avances_type)
        delete_permission = Permission.objects.get(codename="delete_avances", content_type=avances_type)

        programadores_group.permissions.add(add_permission, change_permission, delete_permission)

        programadores_group.save()
        #anadir permiso de reasignacion

        reasignacion_type= ContentType.objects.get_for_model(Reasignacion)
        
        add_permission = Permission.objects.get(codename="add_reasignacion", content_type=reasignacion_type)
        programadores_group.permissions.add(add_permission)
        
        programadores_group.save()

        #crear grupo usuario
        Group.objects.filter(name='clientes').delete()
        
        usuarios_group = Group(name='clientes')
        usuarios_group.save()
        #añadir permiso reportebug
        reportebug_type= ContentType.objects.get_for_model(ReporteBug)
        add_permission = Permission.objects.get(codename="add_reportebug", content_type=reportebug_type)
        usuarios_group.permissions.add(add_permission)
        usuarios_group.save()


        # Insertar un usuario
        usuario = User.objects.create_user(username='MAstroza',password='1234',email='mastroza@udec.cl',is_staff=False)
        usuario.save()

        usuario1 = User.objects.create_user(username='JMartinez',password='1234',email='jmartinez@udec.cl',is_staff=False)
        usuario1.save()

        usuario2 = User.objects.create_user(username='FVidal',password='1234',email='fvidal@udec.cl',is_staff=False)
        usuario2.save()

        usuario3 = User.objects.create_user(username='FBarrera',password='1234',email='fbarrera@udec.cl',is_staff=False)
        usuario3.save()


        # Insertar programadores
        programador1 = User.objects.create_user(username='SSanhueza',first_name='Sebastian',last_name='Sanhueza',password='1234',email='ssanhueza@udec.cl',is_staff=True)
        programador1.save()

        programador2 = User.objects.create_user(username='NHerrera',first_name='Nicolas',last_name='Herrera',password='1234',email='nherrera@udec.cl',is_staff=True)
        programador2.save()

        programador3 = User.objects.create_user(username='RZurita',first_name='Romina',last_name='Zurita',password='1234',email='rzurita@udec.cl',is_staff=True)
        programador3.save()

        programador4 = User.objects.create_user(username='DMichel',first_name='Daniel',last_name='Michel',password='1234',email='dmichel@udec.cl',is_staff=True)
        programador4.save()

        programador5 = User.objects.create_user(username='MVilla',first_name='Miguel',last_name='Villa',password='1234',email='mvilla@udec.cl',is_staff=True)
        programador5.save()

        programador6 = User.objects.create_user(username='YReyes',first_name='Yerko',last_name='Reyes',password='1234',email='yreyes@udec.cl',is_staff=True)
        programador6.save()

        # Insertar proyectos
        proyecto1 = Proyecto.objects.create(nombre_proyecto='Ecommerce Cocacola')
        proyecto1.save()

        proyecto2 = Proyecto.objects.create(nombre_proyecto='Correos Electronicos DTI')
        proyecto2.save()

        # Agregar programadores a los proyectos
        cargo1 = Cargo.objects.create(id_programador=programador1.programador, id_proyecto=proyecto1, cargo='Desarrollador')
        cargo1.save()

        cargo2 = Cargo.objects.create(id_programador=programador2.programador, id_proyecto=proyecto1, cargo='Tester')
        cargo2.save()

        cargo3 = Cargo.objects.create(id_programador=programador3.programador, id_proyecto=proyecto1, cargo='Administrador')
        cargo3.save()

        cargo4 = Cargo.objects.create(id_programador=programador4.programador, id_proyecto=proyecto2, cargo='Administrador')
        cargo4.save()

        cargo5 = Cargo.objects.create(id_programador=programador5.programador, id_proyecto=proyecto2, cargo='Desarrollador')
        cargo5.save()

        cargo6 = Cargo.objects.create(id_programador=programador6.programador, id_proyecto=proyecto2, cargo='Tester')
        cargo6.save()

        # Insertar reportes de bugs
        reporte1 = ReporteBug.objects.create(titulo='Reporte 1', reporte='Reporte del Bug 1',id_usuario=usuario.usuario, id_proyecto=proyecto1)


        reporte2 = ReporteBug.objects.create(titulo='Reporte 2', reporte='Reporte del Bug 2', estado=ReporteBug.ESTADOS_CHOICES[2][0], id_usuario=usuario2.usuario, id_proyecto=proyecto2)
    

        reporte3 = ReporteBug.objects.create(titulo='Reporte 3', reporte='Reporte del Bug 3', estado=ReporteBug.ESTADOS_CHOICES[1][0], id_usuario=usuario3.usuario, id_bug=bug3, id_proyecto=proyecto1)
        

        reporte4 = ReporteBug.objects.create(titulo='Reporte 4', reporte='Reporte del Bug 4', estado=ReporteBug.ESTADOS_CHOICES[1][0], id_usuario=usuario3.usuario, id_bug=bug4, id_proyecto=proyecto2)
        
        
        # Insertar bugs
        bug1 = Bug.objects.create(titulo='Bug 1', descripcion='Cuando voy a agregar una cocacola al carrito, me da error', prioridad=Bug.PRIORIDADES_CHOICES[2][0], estado=Bug.ESTADOS_CHOICES[0][0], id_proyecto=proyecto1, id_programador=programador1.programador)
        bug1.save()

        bug2 = Bug.objects.create(titulo='Bug 2', descripcion='No puedo iniciar sesion desde un nuevo dispositivo, pero desde los viejos funciona bien', prioridad=Bug.PRIORIDADES_CHOICES[0][0], estado=Bug.ESTADOS_CHOICES[1][0], id_proyecto=proyecto2, id_programador=programador1.programador)
        bug2.save()

        bug3 = Bug.objects.create(titulo='Bug 3', descripcion='al momento de agregar mas inventario, la sprite no suman', prioridad=Bug.PRIORIDADES_CHOICES[3][0], estado=Bug.ESTADOS_CHOICES[2][0], id_proyecto=proyecto1, id_programador=programador3.programador)
        bug3.save()

        bug4 = Bug.objects.create(titulo='Bug 4', descripcion='Al adjuntar archivos, los de tipo pdf no se agregan', prioridad=Bug.PRIORIDADES_CHOICES[1][0], estado=Bug.ESTADOS_CHOICES[1][0], id_proyecto=proyecto2, id_programador=programador5.programador)
        bug4.save()


        #Insertar avances
        #avances bug 2 y 4 un avance asignado a cada uno
        #al bug 3 dos avances 
        avances1= Avances.objects.create(titulo='Avance Bug 2', descripcion='inventar', id_bug=bug2)
        avances1.save()

        avances2= Avances.objects.create(titulo='Avance Bug 3', descripcion='inventar', id_bug=bug3)
        avances2.save()

        avances3= Avances.objects.create(titulo='Avance final Bug 3', descripcion='inventar', id_bug=bug3)
        avances3.save()

        avances4= Avances.objects.create(titulo='Avance Bug 4', descripcion='inventar', id_bug=bug4)
        avances4.save()

        #insertar imagenes

        imagen1=Imagen.objects.create(imagen='database/images/2c1cfbd4-87e8-4864-9c81-2f9a99a731ed.webp', id_reporte=reporte1)
        imagen1.save()

        imagen2=Imagen.objects.create(imagen='database/images/734af5af-d132-4310-997c-110150f9d099.webp', id_reporte=reporte2)
        imagen2.save()

        imagen3=Imagen.objects.create(imagen='database/images/34330fe8-8d04-4cd7-9175-43396e39c563.webp', id_reporte=reporte3)
        imagen3.save()

        imagen4=Imagen.objects.create(imagen='database/images/acc81edf-c260-4ce7-9b80-50f8c7e21f47.webp', id_reporte=reporte4)
        imagen4.save()
        
        
        reasignacion1 = Reasignacion.objects.create(id_programador_inicial=programador1.programador,id_bug=bug1)
        reasignacion1.save()
        
        reasignacion2 = Reasignacion.objects.create(id_programador_inicial=programador5.programador,id_bug=bug4)
        reasignacion2.save()
        
        self.stdout.write(self.style.SUCCESS('La base de datos se ha llenado correctamente.'))
        

