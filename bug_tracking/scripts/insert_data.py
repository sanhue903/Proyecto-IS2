

# Importar los modelos
#from django.contrib.auth.models import User
from database.models import Usuario, Programador, Proyecto, Cargo, Bug, ReporteBug
from datetime import datetime

# Crear un usuario
#user = User.objects.create(username='Manuel_Astroza', email='mastroza@udec.cl', password='micontraseña')

# Insertar un usuario
usuario = Usuario.objects.create(correo_usuario='mreyes@cocacola')
usuario.save()

usuario1 = Usuario.objects.create(correo_usuario='lulagos@cocacola.com')
usuario1.save()

usuario2 = Usuario.objects.create(correo_usuario='fevargas@dti.com')
usuario2.save()

usuario3 = Usuario.objects.create(correo_usuario='fvidal@dti.com')
usuario3.save()


# Insertar programadores
programador1 = Programador.objects.create(correo_programador='rosalazar@udec.cl', nombre_programador='Romina Salazar')
programador1.save()

programador2 = Programador.objects.create(correo_programador='sebasanhue@udec.cl', nombre_programador='Sebastian Sanhueza')
programador2.save()

programador3 = Programador.objects.create(correo_programador='hsuazo@udec.cl', nombre_programador='Humberto Suazo')
programador3.save()

programador4 = Programador.objects.create(correo_programador='jtorres@udec.cl', nombre_programador='Jeremias Torres')
programador4.save()

programador5 = Programador.objects.create(correo_programador='cleiva@udec.cl', nombre_programador='Cristobal Leiva')
programador5.save()

programador6 = Programador.objects.create(correo_programador='eparedes@udec.cl', nombre_programador='Esteban Paredes')
programador6.save()

# Insertar proyectos
proyecto1 = Proyecto.objects.create(nombre_proyecto='Ecommerce Cocacola')
proyecto1.save()

proyecto2 = Proyecto.objects.create(nombre_proyecto='Correos Electronicos DTI')
proyecto2.save()

# Agregar programadores a los proyectos
cargo1 = Cargo.objects.create(id_programador=programador1, id_proyecto=proyecto1, cargo='Desarrollador')
cargo1.save()

cargo2 = Cargo.objects.create(id_programador=programador2, id_proyecto=proyecto1, cargo='Tester')
cargo2.save()

cargo3 = Cargo.objects.create(id_programador=programador3, id_proyecto=proyecto1, cargo='Administrador')
cargo3.save()

cargo4 = Cargo.objects.create(id_programador=programador4, id_proyecto=proyecto2, cargo='Administrador')
cargo4.save()

cargo5 = Cargo.objects.create(id_programador=programador5, id_proyecto=proyecto2, cargo='Desarrollador')
cargo5.save()

cargo6 = Cargo.objects.create(id_programador=programador6, id_proyecto=proyecto2, cargo='Tester')
cargo6.save()

# Insertar bugs
bug1 = Bug.objects.create(titulo='Bug 1', descripcion='Cuando voy a agregar una cocacola al carrito, me da error', prioridad='alta', estado='nuevo',fecha_reporte=datetime.now(), id_proyecto=proyecto1, id_programador=programador1)
bug1.save()

bug2 = Bug.objects.create(titulo='Bug 2', descripcion='No puedo iniciar sesion desde un nuevo dispositivo, pero desde los viejos funciona bien',fecha_reporte=datetime.now(), prioridad='baja', estado='en proceso', id_proyecto=proyecto2, id_programador=programador1)
bug2.save()

bug3 = Bug.objects.create(titulo='Bug 3', descripcion='al momento de agregar mas inventario, la sprite no suman', prioridad='baja', estado='nuevo',fecha_reporte=datetime.now(), id_proyecto=proyecto1, id_programador=programador5)
bug3.save()

bug4 = Bug.objects.create(titulo='Bug 4', descripcion='Al adjuntar archivos, los de tipo pdf no se agregan', prioridad='media', estado='en proceso', fecha_reporte=datetime.now(), id_proyecto=proyecto2, id_programador=programador5)
bug4.save()

# Insertar reportes de bugs
reporte1 = ReporteBug.objects.create(titulo='Reporte 1', reporte='Reporte del Bug 1', fecha_reporte=datetime.now(), estado='nuevo',correo_usuario=usuario, id_bug=bug1)
reporte1.save()

reporte2 = ReporteBug.objects.create(titulo='Reporte 2', reporte='Reporte del Bug 2',fecha_reporte=datetime.now(), estado='en proceso', correo_usuario=usuario2, id_bug=bug2)
reporte2.save()

reporte3 = ReporteBug.objects.create(titulo='Reporte 3', reporte='Reporte del Bug 3',fecha_reporte=datetime.now(), estado='nuevo', correo_usuario=usuario3, id_bug=bug3)
reporte3.save()

reporte4 = ReporteBug.objects.create(titulo='Reporte 4', reporte='Reporte del Bug 4', fecha_reporte=datetime.now(), estado='en proceso' , correo_usuario=usuario3, id_bug=bug4)
reporte4.save()
