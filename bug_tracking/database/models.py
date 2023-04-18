from django.db import models

# Create your models here.


class Usuario(models.Model):
    correo_usuario = models.EmailField(primary_key=True)

    def __str__(self):
        return self.correo_usuario

class ReporteBug(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    reporte = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reportes')

    def __str__(self):
        return self.reporte


class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=255, verbose_name='Nombre del proyecto')

    def __str__(self):
        return self.nombre_proyecto

class Programador(models.Model):
    id_programador = models.AutoField(primary_key=True)
    correo_programador = models.EmailField()
    nombre_programador = models.CharField(max_length=255, verbose_name='Nombre del programador')
    

    def __str__(self):
        return self.nombre_programador

