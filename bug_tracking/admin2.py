from django.contrib.auth.models import User
from django.db import models

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Programador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Agrega los campos adicionales necesarios para el modelo Programador
    
    def __str__(self):
        return self.user.username
    

from django.contrib.auth.models import User, Group, Permission

# ...

# Crear el grupo "Usuarios"
group_usuarios, created = Group.objects.get_or_create(name='Usuarios')

# Crear el grupo "Programadores"
group_programadores, created = Group.objects.get_or_create(name='Programadores')

# Asignar los permisos a los grupos correspondientes
reporte_bug_permission = Permission.objects.get(codename='add_reportebug')
group_usuarios.permissions.add(reporte_bug_permission)

avance_permission = Permission.objects.get(codename='add_avance')
reasignacion_permission = Permission.objects.get(codename='add_reasignacion')
group_programadores.permissions.add(avance_permission, reasignacion_permission)

# ...
