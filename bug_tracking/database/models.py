from django.db import models

# Create your models here.


class Usuario(models.Model):
    correo_usuario = models.EmailField(primary_key=True)

    


class Programador(models.Model):
    id_programador = models.AutoField(primary_key=True)
    correo_programador = models.EmailField(null=False)
    nombre_programador = models.CharField(max_length=255, verbose_name='Nombre del programador')
    




class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=255, null=False, verbose_name='Nombre del proyecto')




class ReporteBug(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    reporte = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    correo_usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE, related_name='reportes')




class Prioridad(models.Model):
    PRIORIDADES_CHOICES = (
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("urgente", "Urgente"),
    )
    id_prioridad = models.AutoField(primary_key=True)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES_CHOICES, verbose_name='Prioridad')

 

class Estado(models.Model):
    ESTADOS_CHOICES = (
        ('nuevo', 'Nuevo'),
        ('en proceso', 'En proceso'),
        ('solucionado', 'Solucionado'),
    )

    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, verbose_name='Estado')



class Bug(models.Model):
    id_bug = models.AutoField(primary_key=True)
    descripcion = models.TextField(verbose_name='Descripción')
    prioridad = models.ForeignKey(Prioridad,on_delete=models.CASCADE, verbose_name='Prioridad')
    estado = models.ForeignKey(Estado, null=False, on_delete=models.CASCADE, verbose_name='Estado')
    proyecto = models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE, verbose_name='Proyecto')
    programador = models.ForeignKey(Programador, null=False, on_delete=models.CASCADE, verbose_name='Programador')
    #reportes = models.ManyToManyField(ReporteBug, null=False, related_name='bugs', verbose_name='Reportes')

