from django.db import models

# Create your models here.


class Usuario(models.Model):
    correo_usuario = models.EmailField(primary_key=True)
    
    def __str__(self):
        return self.correo_usuario

    
class Programador(models.Model):
    id_programador     = models.AutoField(primary_key=True)
    correo_programador = models.EmailField(null=False)
    nombre_programador = models.CharField(max_length=255,null=False, verbose_name='Nombre del programador')
    
    def __str__(self):
        return self.nombre_programador
    
    class Meta:
        verbose_name_plural = "Programadores"
    

class Proyecto(models.Model):
    id_proyecto     = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=255, null=False, verbose_name='Nombre del proyecto')
    
    programadores   = models.ManyToManyField(Programador, through="Cargo")

    def __str__(self):
        return self.nombre_proyecto

class Cargo(models.Model):
    id_programador = models.ForeignKey(Programador, null=False, on_delete=models.CASCADE)
    id_proyecto    = models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE)
    
    cargo          = models.CharField(max_length=255, null=False, verbose_name='Cargo en el proyecto')


class Bug(models.Model):
    PRIORIDADES_CHOICES = (
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("urgente", "Urgente"),
    )
    
    ESTADOS_CHOICES = (
        ('nuevo', 'Nuevo'),
        ('en proceso', 'En proceso'),
        ('solucionado', 'Solucionado'),
    )
    
    id_bug         = models.AutoField(primary_key=True)
    titulo         = models.CharField(max_length=255, null=False, verbose_name='Titulo del bug')
    descripcion    = models.TextField(null=False, verbose_name='Descripción')
    prioridad      = models.CharField(max_length=20, choices=PRIORIDADES_CHOICES, verbose_name='Prioridad')
    estado         = models.CharField(max_length=20, choices=ESTADOS_CHOICES, verbose_name='Estado')
    fecha_reporte  = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    
    id_proyecto    = models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE, verbose_name='Proyecto')
    id_programador = models.ForeignKey(Programador, null=False, on_delete=models.CASCADE, verbose_name='Programador')
    
    def __str__(self):
        return str(self.id_bug)

    
class ReporteBug(models.Model):
    id_reporte     = models.AutoField(primary_key=True)
    titulo         = models.CharField(max_length=255, null=False, verbose_name='titulo del reporte')
    reporte        = models.TextField(null=False)
    fecha_reporte  = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    
    correo_usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE, related_name='reportes')
    id_bug         = models.ForeignKey(Bug, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Bug')

    def __str__(self):
        return self.titulo
    
