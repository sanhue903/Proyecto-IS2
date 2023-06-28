from database.models import *
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.wsgi import get_wsgi_application
from django.core.management.base import BaseCommand, CommandError

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bug_tracking.settings")
application = get_wsgi_application()

# Importar los modelos
#from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.filter(name='empleados').delete()
        
        programadores_group = Group(name='empleados')
        programadores_group.save()

        #añadir permisos para editar objetos del modelo Avances
        avances_type = ContentType.objects.get_for_model(Avances)

        add_permission = Permission.objects.get(codename="add_avances", content_type=avances_type)
        change_permission = Permission.objects.get(codename="change_avances", content_type=avances_type)
        delete_permission = Permission.objects.get(codename="delete_avances", content_type=avances_type)

        programadores_group.permissions.add(add_permission, change_permission, delete_permission)

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
        proyecto3 = Proyecto.objects.create(nombre_proyecto='Servicio de Horas de atencion Municipalidad de THNO')
        proyecto3.save()

        proyecto4 = Proyecto.objects.create(nombre_proyecto='Facebook')
        proyecto4.save()

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


        # Insertar bugs
        bug1 = Bug.objects.create(titulo='Bug 1', descripcion='Cuando voy a agregar una cocacola al carrito, me da error', prioridad=('ALTA', 'bug de alta prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto1, id_programador=programador1.programador)
        bug1.save()

        bug2 = Bug.objects.create(titulo='Bug 2', descripcion='No puedo iniciar sesion desde un nuevo dispositivo, pero desde los viejos funciona bien', prioridad=('BAJA', 'bug de baja prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador1.programador)
        bug2.save()

        bug3 = Bug.objects.create(titulo='Bug 3', descripcion='al momento de agregar mas bebidas al inventario, la sprite no suman', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto1, id_programador=programador3.programador)
        bug3.save()

        bug4 = Bug.objects.create(titulo='Bug 4', descripcion='Al adjuntar archivos, los de tipo pdf no se agregan', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador5.programador)
        bug4.save()

        bug5= Bug.objects.create(titulo='Bug 5', descripcion='Al momento de pedir una hora, esta no me entrega confirmacion y vuelve al inicio', prioridad=('ALTA', 'bug de alta prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto3, id_programador=programador1.programador)
        bug5.save()

        bug6 = Bug.objects.create(titulo='Bug 6', descripcion='Cuando ya llene mi carrito de compras, cuando quiero pagar este se borra', prioridad=('BAJA', 'bug de baja prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador1.programador)
        bug6.save()

        bug7 = Bug.objects.create(titulo='Bug 7', descripcion='Al momento de agregar el correo, la pagina no lo verifica', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto3, id_programador=programador3.programador)
        bug7.save()

        bug8 = Bug.objects.create(titulo='Bug 8', descripcion='Cuando quiero pagar, no me manda a la pagina del banco y no me deja finalizar la compra', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador5.programador)
        bug8.save()

        bug9 = Bug.objects.create(titulo='Bug 9', descripcion='El enlace de restablecimiento de contraseña no funciona correctamente y no permite a los usuarios cambiar su contraseña', prioridad=('ALTA', 'Bug de alta prioridad'), estado=('PENDIENTE', 'Bug pendiente de revisión'), id_proyecto=proyecto4, id_programador=programador3.programador)
        bug9.save()

        bug10 = Bug.objects.create(titulo='Bug 10', descripcion='La funcionalidad de búsqueda no muestra resultados precisos y devuelve datos incorrectos', prioridad=('MEDIA', 'Bug de media prioridad'), estado=('EN PROCESO', 'Bug en proceso de revisión'), id_proyecto=proyecto1, id_programador=programador1.programador)
        bug10.save()

        bug11 = Bug.objects.create(titulo='Bug 11', descripcion='La imagen de perfil del usuario no se muestra correctamente y aparece distorsionada', prioridad=('ALTA', 'bug de alta prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto4, id_programador=programador3.programador)
        bug11.save()

        bug12 = Bug.objects.create(titulo='Bug 12', descripcion='La funcionalidad de agregar productos al carrito no funciona y los artículos no se agregan correctamente', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador3.programador)
        bug12.save()

        bug13 = Bug.objects.create(titulo='Bug 13', descripcion='El proceso de pago muestra un error al ingresar los detalles de la tarjeta de crédito', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador2.programador)
        bug13.save()

        bug14 = Bug.objects.create(titulo='Bug 14', descripcion='Los usuarios no pueden iniciar sesión con sus cuentas de Google y se muestra un error de autenticación', prioridad=('BAJA', 'bug de baja prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug14.save()

        bug15 = Bug.objects.create(titulo='Bug 15', descripcion='La funcionalidad de compartir en redes sociales no muestra los enlaces correctos y no comparte la información adecuada', prioridad=('ALTA', 'bug de alta prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador4.programador)
        bug15.save()

        bug16 = Bug.objects.create(titulo='Bug 16', descripcion='Al enviar el formulario de contacto, los datos no se envían por correo electrónico al destinatario', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador1.programador)
        bug16.save()

        bug17 = Bug.objects.create(titulo='Bug 17', descripcion='La página de perfil del usuario muestra información incorrecta y no se actualiza correctamente', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador2.programador)
        bug17.save()

        bug18 = Bug.objects.create(titulo='Bug 18', descripcion='El botón de inicio de sesión no funciona y no permite a los usuarios acceder al sistema', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto3, id_programador=programador3.programador)
        bug18.save()

        bug19 = Bug.objects.create(titulo='Bug 19', descripcion='El botón de "Guardar cambios" no está funcionando correctamente y no guarda las modificaciones realizadas en el formulario.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto1, id_programador=programador4.programador)
        bug19.save()

        bug20 = Bug.objects.create(titulo='Bug 20', descripcion=' La página de inicio muestra contenido duplicado, lo cual genera confusión entre los usuarios.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug20.save()

        bug21 = Bug.objects.create(titulo='Bug 21', descripcion='Al realizar una búsqueda en el sistema, algunos resultados no se muestran correctamente y aparecen datos incorrectos.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto3, id_programador=programador2.programador)
        bug21.save()

        bug22 = Bug.objects.create(titulo='Bug 22', descripcion='La funcionalidad de cargar archivos no permite subir archivos de gran tamaño y muestra un mensaje de error.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador3.programador)
        bug22.save()

        bug23 = Bug.objects.create(titulo='Bug 23', descripcion='La aplicación se bloquea aleatoriamente al intentar acceder a ciertas secciones del sistema.', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto4, id_programador=programador4.programador)
        bug23.save()

        bug24 = Bug.objects.create(titulo='Bug 24', descripcion='Los mensajes de notificación no se muestran correctamente y algunos usuarios no reciben las alertas correspondientes.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug24.save()

        bug25 = Bug.objects.create(titulo='Bug 25', descripcion='Al intentar enviar un formulario, los campos obligatorios no están siendo validados correctamente y permite enviar datos incompletos.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto2, id_programador=programador2.programador)
        bug25.save()

        bug26 = Bug.objects.create(titulo='Bug 26', descripcion=' La interfaz de usuario presenta problemas de diseño en dispositivos móviles, lo que dificulta la navegación y visualización adecuada.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto4, id_programador=programador3.programador)
        bug26.save()

        bug27 = Bug.objects.create(titulo='Bug 27', descripcion='Al realizar una acción determinada, el sistema genera un error interno del servidor y muestra una página en blanco.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto3, id_programador=programador4.programador)
        bug27.save()
        
        bug28 = Bug.objects.create(titulo='Bug 28', descripcion='Al intentar acceder a un enlace específico, se muestra un error 404 indicando que la página no se encuentra disponible.', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador1.programador)
        bug28.save()

        bug29 = Bug.objects.create(titulo='Bug 29', descripcion=' El sistema no permite iniciar sesión con ciertos caracteres especiales en la contraseña, generando un mensaje de error incorrecto.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador2.programador)
        bug29.save()

        bug30 = Bug.objects.create(titulo='Bug 30', descripcion='Al intentar realizar una compra, el monto total se calcula incorrectamente y muestra un valor incorrecto en el resumen de la transacción.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador3.programador)
        bug30.save()

        bug31 = Bug.objects.create(titulo='Bug 31', descripcion='El sistema no guarda correctamente el historial de actividades de los usuarios, lo que dificulta el seguimiento de las acciones realizadas.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto3, id_programador=programador4.programador)
        bug31.save()

        bug32 = Bug.objects.create(titulo='Bug 32', descripcion='Al subir una imagen como avatar de usuario, la imagen no se muestra correctamente y aparece distorsionada en la interfaz.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug32.save()

        bug33 = Bug.objects.create(titulo='Bug 33', descripcion='La función de autocompletado en un campo de búsqueda no muestra los resultados correspondientes a medida que se escriben las letras.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto4, id_programador=programador2.programador)
        bug33.save()

        bug34 = Bug.objects.create(titulo='Bug 34', descripcion='Al seleccionar una opción del menú principal, la página se carga en blanco y no muestra el contenido esperado.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto1, id_programador=programador3.programador)
        bug34.save()

        bug35 = Bug.objects.create(titulo='Bug 35', descripcion='Al intentar guardar un archivo adjunto en un formulario, el sistema genera un error de "archivo no válido" aunque cumple con los requisitos establecidos.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador4.programador)
        bug35.save()

        bug36 = Bug.objects.create(titulo='Bug 36', descripcion=' El sistema no muestra correctamente los acentos y caracteres especiales en los textos, generando errores de visualización y lectura.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador1.programador)
        bug36.save()

        bug37 = Bug.objects.create(titulo='Bug 37', descripcion='Al realizar una acción específica, como eliminar un elemento, el sistema no actualiza automáticamente la interfaz y muestra el elemento eliminado.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto3, id_programador=programador2.programador)
        bug37.save()

        bug38 = Bug.objects.create(titulo='Bug 38', descripcion='Al intentar realizar una exportación de datos, el archivo descargado está vacío o presenta información incompleta.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador3.programador)
        bug38.save()

        bug39 = Bug.objects.create(titulo='Bug 39', descripcion='El sistema no valida correctamente los formatos de fecha ingresados y permite introducir fechas inválidas.', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto3, id_programador=programador4.programador)
        bug39.save()

        bug40 = Bug.objects.create(titulo='Bug 40', descripcion='Al cargar un video en el sistema, el reproductor no reproduce el archivo correctamente y muestra un mensaje de error.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug40.save()

        bug41 = Bug.objects.create(titulo='Bug 41', descripcion='La función de generación de informes no muestra todos los datos requeridos y omite cierta información en el archivo generado.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador2.programador)
        bug41.save()

        bug42 = Bug.objects.create(titulo='Bug 42', descripcion='Al realizar una operación de filtrado en una tabla de datos, algunos elementos no se muestran correctamente y se omiten del resultado.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto3, id_programador=programador3.programador)
        bug42.save()

        bug43 = Bug.objects.create(titulo='Bug 43', descripcion='El sistema muestra un mensaje de error genérico al intentar realizar una acción sin proporcionar la información necesaria, lo que dificulta la identificación del problema.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto2, id_programador=programador4.programador)
        bug43.save()

        bug44 = Bug.objects.create(titulo='Bug 44', descripcion='Al realizar una búsqueda por categoría en un sistema de e-commerce, no se muestran todos los productos correspondientes a la categoría seleccionada.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto1, id_programador=programador1.programador)
        bug44.save()

        bug45 = Bug.objects.create(titulo='Bug 45', descripcion='El sistema no guarda correctamente las preferencias de idioma del usuario y muestra el idioma predeterminado en lugar de la selección realizada.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto3, id_programador=programador2.programador)
        bug45.save()

        bug46 = Bug.objects.create(titulo='Bug 46', descripcion='Al crear un nuevo usuario, el sistema permite ingresar una contraseña débil sin mostrar un mensaje de advertencia.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto4, id_programador=programador3.programador)
        bug46.save()

        bug47 = Bug.objects.create(titulo='Bug 47', descripcion='Al intentar guardar una publicación en un blog, el sistema no muestra los estilos de formato aplicados y muestra el texto sin formato.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto4, id_programador=programador4.programador)
        bug47.save()

        bug48 = Bug.objects.create(titulo='Bug 48', descripcion='Al realizar una acción de edición en un formulario, algunos campos no se guardan correctamente y muestran valores anteriores.', prioridad=('URGENTE', 'bug de urgente prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto3, id_programador=programador1.programador)
        bug48.save()

        bug49 = Bug.objects.create(titulo='Bug 49', descripcion='La función de envío de correos electrónicos no se ejecuta correctamente y los usuarios no reciben las notificaciones correspondientes.', prioridad=('ALTA', 'bug de alta prioridad'), estado=('EN PROCESO', 'bug esta proceso de revisión'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug49.save()

        bug50 = Bug.objects.create(titulo='Bug 50', descripcion='Al intentar realizar una importación masiva de datos, el sistema muestra un error de "archivo no encontrado" aunque el archivo esté presente.', prioridad=('BAJA', 'bug de baja prioridad'), estado=('SOLUCIONADO', 'bug solucionado'), id_proyecto=proyecto2, id_programador=programador2.programador)
        bug50.save()

        bug51 = Bug.objects.create(titulo='Bug 51', descripcion='Al seleccionar una opción del menú desplegable, la lista de opciones se despliega detrás de otros elementos y no es visible para el usuario.', prioridad=('MEDIA', 'bug de media prioridad'), estado=('ASIGNADO', 'bug recien asignado'), id_proyecto=proyecto4, id_programador=programador1.programador)
        bug51.save()

        # Insertar reportes de bugs
        # agregar challa a descripcion de pelicula
        reporte1 = ReporteBug.objects.create(titulo='Reporte 1', reporte='Reporte sobre el carrito de comprar, no funciona', estado=('PENDIENTE', 'reporte en estado pendiente'),id_usuario=usuario.usuario, id_proyecto=proyecto1)
        reporte1.save()

        reporte2 = ReporteBug.objects.create(titulo='Reporte 2', reporte='Reporte sobre el inicio de sesión en nuevos dispositivos', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario2.usuario, id_proyecto=proyecto2)
        reporte2.save()

        reporte3 = ReporteBug.objects.create(titulo='Reporte 3', reporte='Reporte sobre el la funcion para pedir de horas', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug3, id_proyecto=proyecto1)
        reporte3.save()

        reporte4 = ReporteBug.objects.create(titulo='Reporte 4', reporte='Reporte de adjuntar archivos al correo', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug4, id_proyecto=proyecto2)
        reporte4.save()

        reporte5 = ReporteBug.objects.create(titulo='Reporte 5', reporte='Reporte sobre el la funcion para pedir de horas', estado=('PENDIENTE', 'reporte en estado pendiente'),id_usuario=usuario.usuario, id_proyecto=proyecto3)
        reporte5.save()

        reporte6 = ReporteBug.objects.create(titulo='Reporte 6', reporte='Reporte sobre el momento de recibir un pago', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario2.usuario, id_proyecto=proyecto1)
        reporte6.save()

        reporte7 = ReporteBug.objects.create(titulo='Reporte 7', reporte='Reporte de la veficacion de las cuentas', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug7, id_proyecto=proyecto3)
        reporte7.save()

        reporte8 = ReporteBug.objects.create(titulo='Reporte 8', reporte='Reporte del momento de recibir un pago', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug8, id_proyecto=proyecto1)
        reporte8.save()

        reporte9 = ReporteBug.objects.create(titulo='Reporte 9', reporte='Reporte de reestablecer contraseña', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario1.usuario, id_bug=bug9, id_proyecto=proyecto4)
        reporte9.save()

        reporte10 = ReporteBug.objects.create(titulo='Reporte 10', reporte='Reporte De la funcionalidad de busqueda', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario2.usuario, id_bug=bug10, id_proyecto=proyecto1)
        reporte10.save()

        reporte11 = ReporteBug.objects.create(titulo='Reporte 11', reporte='Reporte de la imagen de perfil  ', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario3.usuario, id_bug=bug11, id_proyecto=proyecto4)
        reporte11.save()

        reporte12 = ReporteBug.objects.create(titulo='Reporte 12', reporte='Reporte sobre agregar productos al carrito ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario.usuario, id_bug=bug12, id_proyecto=proyecto1)
        reporte12.save()

        reporte13 = ReporteBug.objects.create(titulo='Reporte 13', reporte='Reporte en el proceso del pago ', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario1.usuario, id_bug=bug13, id_proyecto=proyecto1)
        reporte13.save()

        reporte14 = ReporteBug.objects.create(titulo='Reporte 14', reporte='Reporte sobre el inicio de sesión con cuenta google ', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario2.usuario, id_bug=bug14, id_proyecto=proyecto4)
        reporte14.save()

        reporte15 = ReporteBug.objects.create(titulo='Reporte 15', reporte='Reporte compartir el enlace a otras redes sociales ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug15, id_proyecto=proyecto4)
        reporte15.save()

        reporte16 = ReporteBug.objects.create(titulo='Reporte 16', reporte='Reporte sobre el formulario de contactos ', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario1.usuario, id_bug=bug16, id_proyecto=proyecto2)
        reporte16.save()

        reporte17 = ReporteBug.objects.create(titulo='Reporte 17', reporte='Reporte de la pagina de perfil repetida y en mal estado ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario2.usuario, id_bug=bug17, id_proyecto=proyecto4)
        reporte17.save()

        reporte18 = ReporteBug.objects.create(titulo='Reporte 18', reporte='Reporte sobre el boton de inicio', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug18, id_proyecto=proyecto3)
        reporte18.save()

        reporte19 = ReporteBug.objects.create(titulo='Reporte 19', reporte='Reporte sobre el boton de guardar los cambios', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario.usuario, id_bug=bug19, id_proyecto=proyecto1)
        reporte19.save()

        reporte20 = ReporteBug.objects.create(titulo='Reporte 20', reporte='Reporte de la pagina de inicio duplivada', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario1.usuario, id_bug=bug20, id_proyecto=proyecto4)
        reporte20.save()

        reporte21 = ReporteBug.objects.create(titulo='Reporte 21', reporte='Reporte sobre la busqueda en el sistema ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario2.usuario, id_bug=bug21, id_proyecto=proyecto3)
        reporte21.save()

        reporte22 = ReporteBug.objects.create(titulo='Reporte 22', reporte='Reporte en la carga de archivos, no permiten los de gran tamaño ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug22, id_proyecto=proyecto2)
        reporte22.save()

        reporte23 = ReporteBug.objects.create(titulo='Reporte 23', reporte='Reporte sobre un bloqueo aleatorio a ciertas secciones del sistema ', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario.usuario, id_bug=bug23, id_proyecto=proyecto4)
        reporte23.save()

        reporte24 = ReporteBug.objects.create(titulo='Reporte 24', reporte='Reporte en el mensaje de notificaciones', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario1.usuario, id_bug=bug24, id_proyecto=proyecto4)
        reporte24.save()

        reporte25 = ReporteBug.objects.create(titulo='Reporte 25', reporte='Reporte no validan los campos obligatorios ', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario2.usuario, id_bug=bug25, id_proyecto=proyecto2)
        reporte25.save()

        reporte26 = ReporteBug.objects.create(titulo='Reporte 26', reporte='Reporte en la interfaz de usuarios', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario3.usuario, id_bug=bug26, id_proyecto=proyecto4)
        reporte26.save()

        reporte27 = ReporteBug.objects.create(titulo='Reporte 27', reporte='Reporte genera errores y muentra una pagina en blanco ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario.usuario, id_bug=bug27, id_proyecto=proyecto3)
        reporte27.save()

        reporte28 = ReporteBug.objects.create(titulo='Reporte 28', reporte='Reporte de un error 404 ', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario1.usuario, id_bug=bug28, id_proyecto=proyecto1)
        reporte28.save()

        reporte29 = ReporteBug.objects.create(titulo='Reporte 29', reporte='Reporte sobre que no se puede iniciar sesión ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario2.usuario, id_bug=bug29, id_proyecto=proyecto4)
        reporte29.save()

        reporte30 = ReporteBug.objects.create(titulo='Reporte 30', reporte='Reporte en el momento de la compra', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug30, id_proyecto=proyecto1)
        reporte30.save()

        reporte31 = ReporteBug.objects.create(titulo='Reporte 31', reporte='Reporte en el historial del usuario ', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario.usuario, id_bug=bug31, id_proyecto=proyecto3)
        reporte31.save()

        reporte32 = ReporteBug.objects.create(titulo='Reporte 32', reporte='Reporte al subir una imagen de avatar ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario1.usuario, id_bug=bug32, id_proyecto=proyecto4)
        reporte32.save()

        reporte33 = ReporteBug.objects.create(titulo='Reporte 33', reporte='Reporte en la funcion de autocompletado ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario2.usuario, id_bug=bug33, id_proyecto=proyecto4)
        reporte33.save()

        reporte34 = ReporteBug.objects.create(titulo='Reporte 34', reporte='Reporte en la opción de menu principal ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug34, id_proyecto=proyecto1)
        reporte34.save()

        reporte35 = ReporteBug.objects.create(titulo='Reporte 35', reporte='Reporte en el guardar un archivo en el formulario ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario.usuario, id_bug=bug35, id_proyecto=proyecto2)
        reporte35.save()

        reporte36 = ReporteBug.objects.create(titulo='Reporte 36', reporte='Reporte de que no muestra los caracteres de manera correcta ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario1.usuario, id_bug=bug36, id_proyecto=proyecto2)
        reporte36.save()

        reporte37 = ReporteBug.objects.create(titulo='Reporte 37', reporte='Reporte al momento de eliminar un elemento', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario2.usuario, id_bug=bug37, id_proyecto=proyecto3)
        reporte37.save()

        reporte38 = ReporteBug.objects.create(titulo='Reporte 38', reporte='Reporte en la exportacion de datos ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug38, id_proyecto=proyecto4)
        reporte38.save()

        reporte39 = ReporteBug.objects.create(titulo='Reporte 39', reporte='Reporte que no salen bien las fechas ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario.usuario, id_bug=bug39, id_proyecto=proyecto3)
        reporte39.save()

        reporte40 = ReporteBug.objects.create(titulo='Reporte 40', reporte='Reporte sobre la no carga de un video en el sistema', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario1.usuario, id_bug=bug40, id_proyecto=proyecto4)
        reporte40.save()

        reporte41 = ReporteBug.objects.create(titulo='Reporte 41', reporte='Reporte sobre que el sistema genera archivos en los que omite información ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario2.usuario, id_bug=bug41, id_proyecto=proyecto2)
        reporte41.save()

        reporte42 = ReporteBug.objects.create(titulo='Reporte 42', reporte='Reporte que se esta haciendo un filtrado incorrecto ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug42, id_proyecto=proyecto3)
        reporte42.save()

        reporte43 = ReporteBug.objects.create(titulo='Reporte 43', reporte='Reporte se muestra un mensaje de error', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario.usuario, id_bug=bug43, id_proyecto=proyecto2)
        reporte43.save()

        reporte44 = ReporteBug.objects.create(titulo='Reporte 44', reporte='Reporte en los que no se registran los productos', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario1.usuario, id_bug=bug44, id_proyecto=proyecto1)
        reporte44.save()

        reporte45 = ReporteBug.objects.create(titulo='Reporte 45', reporte='Reporte sobre que no se guarda el idioma seleccionado ', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario2.usuario, id_bug=bug45, id_proyecto=proyecto3)
        reporte45.save()

        reporte46 = ReporteBug.objects.create(titulo='Reporte 46', reporte='Reporte de crear un nuevo usuario ', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario3.usuario, id_bug=bug46, id_proyecto=proyecto4)
        reporte46.save()

        reporte47 = ReporteBug.objects.create(titulo='Reporte 47', reporte='Reporte agregar una nueva publicacion al blog ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario.usuario, id_bug=bug47, id_proyecto=proyecto4)
        reporte47.save()

        reporte48 = ReporteBug.objects.create(titulo='Reporte 48', reporte='Reporte sobre que no se puede editar el formulario ', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario1.usuario, id_bug=bug48, id_proyecto=proyecto3)
        reporte48.save()

        reporte49 = ReporteBug.objects.create(titulo='Reporte 49', reporte='Reporte de la funcion de enviar correos ', estado=('DESAPROBADO', 'reporte desaprobado'), id_usuario=usuario2.usuario, id_bug=bug49, id_proyecto=proyecto4)
        reporte49.save()

        reporte50 = ReporteBug.objects.create(titulo='Reporte 50', reporte='Reporte sobre la importacion masiva de datos', estado=('APROBADO', 'reporte aprobado'), id_usuario=usuario3.usuario, id_bug=bug50, id_proyecto=proyecto2)
        reporte50.save()

        reporte51 = ReporteBug.objects.create(titulo='Reporte 51', reporte='Reporte sobre la seleccion de un menu desplegable', estado=('PENDIENTE', 'reporte en estado pendiente'), id_usuario=usuario1.usuario, id_bug=bug51, id_proyecto=proyecto4)
        reporte51.save()


        #Insertar avances
        #avances bug 2 y 4 un avance asignado a cada uno
        #al bug 3 dos avances 

        avances1= Avances.objects.create(titulo='Avance Bug 2', descripcion='Mal uso del usuario, se rechaza el bug', id_bug=bug2)
        avances1.save()

        avances2= Avances.objects.create(titulo='Avance Bug 3', descripcion='Revision primaria del bug, buscando el error', id_bug=bug3)
        avances2.save()

        avances3= Avances.objects.create(titulo='Avance final Bug 3', descripcion='Bug corregido, ahora todas las bebidas se agregan al carrito', id_bug=bug3)
        avances3.save()

        avances4= Avances.objects.create(titulo='Avance Bug 4', descripcion='Correccion con los archivos del tipo pdf', id_bug=bug4)
        avances4.save()

        avances5= Avances.objects.create(titulo='Avance Bug 6', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug6)
        avances5.save()

        avances6= Avances.objects.create(titulo='Avance Bug 7', descripcion='Revision inicial, buscando errores porque no verifica el correo', id_bug=bug7)
        avances6.save()

        avances7= Avances.objects.create(titulo='Avance final Bug 7', descripcion='Bug corregido, el correo ya es verificado', id_bug=bug7)
        avances7.save()

        avances8= Avances.objects.create(titulo='Avance Bug 8', descripcion='El problema de redireccionamiento esta solucionado, se puede comprar con normalidad', id_bug=bug8)
        avances8.save()

        avances9= Avances.objects.create(titulo='Avance Bug 10 ', descripcion='Revision inicial, buscando errores', id_bug=bug10)
        avances9.save()
        
        avances10= Avances.objects.create(titulo='Avance Bug 12', descripcion='Revision inicial, buscando errores', id_bug=bug12)
        avances10.save()

        avances11= Avances.objects.create(titulo='Avance Bug 13', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug13)
        avances11.save()

        avances12= Avances.objects.create(titulo='Avance Bug 15', descripcion='Revision inicial, buscando errores', id_bug=bug15)
        avances12.save()

        avances13= Avances.objects.create(titulo='Avance Final Bug 15', descripcion='Bug corregido', id_bug=bug15)
        avances13.save()

        avances14= Avances.objects.create(titulo='Avance Bug 16', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug16)
        avances14.save()

        avances15= Avances.objects.create(titulo='Avance Bug 17', descripcion='Revision inicial, buscando errores', id_bug=bug17)
        avances15.save()

        avances16= Avances.objects.create(titulo='Avance Final Bug 17', descripcion='Bug corregido', id_bug=bug17)
        avances16.save()

        avances17= Avances.objects.create(titulo='Avance Bug 18', descripcion='Revision inicial, buscando errores', id_bug=bug18)
        avances17.save()

        avances18= Avances.objects.create(titulo='Avance Bug 20', descripcion='Revision inicial, buscando errores', id_bug=bug20)
        avances18.save()

        avances19= Avances.objects.create(titulo='Avance Bug 21', descripcion='Revision inicial, buscando errores', id_bug=bug21)
        avances19.save()
        
        avances20= Avances.objects.create(titulo='Avance Bug 21', descripcion='Revision inicial, buscando errores', id_bug=bug21)
        avances20.save()

        avances21= Avances.objects.create(titulo='Avance Bug 23', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug23)
        avances21.save()

        avances22= Avances.objects.create(titulo='Avance Bug 24', descripcion='Revision inicial, buscando errores', id_bug=bug24)
        avances22.save()

        avances23= Avances.objects.create(titulo='Avance Final Bug 24', descripcion='Revision inicial, buscando errores', id_bug=bug24)
        avances23.save()

        avances24= Avances.objects.create(titulo='Avance Bug 26', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug26)
        avances24.save()

        avances25= Avances.objects.create(titulo='Avance Bug 27', descripcion='Revision inicial, buscando errores', id_bug=bug27)
        avances25.save()

        avances26= Avances.objects.create(titulo='Avance Final Bug 27', descripcion='Bug corregido', id_bug=bug27)
        avances26.save()

        avances27= Avances.objects.create(titulo='Avance Bug 28', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug28)
        avances27.save()

        avances28= Avances.objects.create(titulo='Avance Bug 29', descripcion='Revision inicial, buscando errores', id_bug=bug29)
        avances28.save()

        avances29= Avances.objects.create(titulo='Avance Final Bug 29', descripcion='Bug corregido', id_bug=bug29)
        avances29.save()
        
        avances30= Avances.objects.create(titulo='Avance Bug 30', descripcion='Revision inicial, buscando errores', id_bug=bug30)
        avances30.save()

        avances31= Avances.objects.create(titulo='Avance Bug 32', descripcion='Revision inicial, buscando errores', id_bug=bug32)
        avances31.save()

        avances32= Avances.objects.create(titulo='Avance Final Bug 32', descripcion='Bug corregido', id_bug=bug32)
        avances32.save()

        avances33= Avances.objects.create(titulo='Avance Bug 33', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug33)
        avances33.save()

        avances34= Avances.objects.create(titulo='Avance Bug 34', descripcion='Revision inicial, buscando errores', id_bug=bug34)
        avances34.save()

        avances35= Avances.objects.create(titulo='Avance Final Bug 34', descripcion='Bug corregido', id_bug=bug34)
        avances35.save()

        avances36= Avances.objects.create(titulo='Avance Bug 36', descripcion='Revision inicial, buscando errores', id_bug=bug36)
        avances36.save()

        avances37= Avances.objects.create(titulo='Avance Bug 38', descripcion='Revision inicial, buscando errores', id_bug=bug38)
        avances37.save()

        avances38= Avances.objects.create(titulo='Avance Final Bug 38', descripcion='Bug corregido', id_bug=bug38)
        avances38.save()

        avances39= Avances.objects.create(titulo='Avance Bug 39', descripcion='Revision inicial, buscando errores', id_bug=bug39)
        avances39.save()
        
        avances40= Avances.objects.create(titulo='Avance Bug 41', descripcion='Revision inicial, buscando errores', id_bug=bug41)
        avances40.save()

        avances41= Avances.objects.create(titulo='Avance Bug 42', descripcion='Revision inicial, buscando errores', id_bug=bug42)
        avances41.save()

        avances42= Avances.objects.create(titulo='Avance  Final Bug 42', descripcion='Bug corregido', id_bug=bug42)
        avances42.save()

        avances43= Avances.objects.create(titulo='Avance Bug 43', descripcion='Revision inicial, buscando errores', id_bug=bug43)
        avances43.save()

        avances44= Avances.objects.create(titulo='Avance Bug 44', descripcion='Mal uso del usuario se rechaza el bug', id_bug=bug44)
        avances44.save()

        avances45= Avances.objects.create(titulo='Avance Bug 47', descripcion='Revision inicial, buscando errores', id_bug=bug47)
        avances45.save()

        avances46= Avances.objects.create(titulo='Avance Final Bug 47', descripcion='Bug corregido', id_bug=bug47)
        avances46.save()

        avances47= Avances.objects.create(titulo='Avance Bug 48', descripcion='Revision inicial, buscando errores', id_bug=bug48)
        avances47.save()

        avances48= Avances.objects.create(titulo='Avance Bug 50', descripcion='Revision inicial, buscando errores', id_bug=bug50)
        avances48.save()
        
        avances49= Avances.objects.create(titulo='Avance Final Bug 50', descripcion='Bug corregido', id_bug=bug50)
        avances49.save()



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
        
       
        
        

