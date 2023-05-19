from django.db import models

# Create your models here.


class Usuario(models.Model):
    id_usuario     = models.AutoField(primary_key=True)
    correo_usuario = models.EmailField(unique=True, verbose_name='Email')
    
    def __str__(self):
        return self.correo_usuario

    
class Programador(models.Model):    
    id_programador     = models.AutoField(primary_key=True)
    correo_programador = models.EmailField(null=False, verbose_name='Email')
    nombre_programador = models.CharField(max_length=255,null=False, verbose_name='Empleado')
    
    def __str__(self):
        return self.nombre_programador
    
    class Meta:
        verbose_name_plural = "Programadores"
    

class Proyecto(models.Model):
    id_proyecto     = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=255, null=False, verbose_name='Proyecto')
    
    programadores   = models.ManyToManyField(Programador, through="Cargo")

    def __str__(self):
        return self.nombre_proyecto

class Cargo(models.Model):
    id_programador = models.ForeignKey(Programador, verbose_name='Empleado', null=False, on_delete=models.CASCADE)
    id_proyecto    = models.ForeignKey(Proyecto, verbose_name='Proyecto', null=False, on_delete=models.CASCADE)
    
    cargo          = models.CharField(max_length=255, null=False, verbose_name='Cargo')


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
    titulo         = models.CharField(max_length=255,blank=False, null=False, verbose_name='Titulo del bug')
    descripcion    = models.TextField(null=False, verbose_name='Descripción')
    prioridad      = models.CharField(max_length=20, choices=PRIORIDADES_CHOICES, verbose_name='Prioridad')
    estado         = models.CharField(max_length=20, choices=ESTADOS_CHOICES, verbose_name='Estado')
    fecha_reporte  = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    
    id_proyecto    = models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE, verbose_name='Proyecto')
    id_programador = models.ForeignKey(Programador, null=False, on_delete=models.CASCADE, verbose_name='Programador')
    
    def __str__(self):
        return str(self.id_bug)

    
class ReporteBug(models.Model):
    ESTADOS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('desaprobado', 'Desaprobado')
    )
    
    
    id_reporte    = models.AutoField(primary_key=True)
    titulo        = models.CharField(max_length=255, null=False, verbose_name='titulo del reporte')
    reporte       = models.TextField(null=False)
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    estado        = models.CharField(max_length=20, default='Pendiente', choices=ESTADOS_CHOICES, verbose_name='Estado')
    
    id_usuario    = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE, verbose_name='Usuario', related_name='reportes')
    id_proyecto   = models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE, verbose_name='Proyecto')
    id_bug        = models.ForeignKey(Bug, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Bug')

    def __str__(self):
        return self.titulo

class Imagen(models.Model):
    id_imagen  = models.AutoField(primary_key=True)
    imagen     = models.ImageField(null=False,upload_to="") #definir ruta
    
    id_reporte = models.ForeignKey(ReporteBug, null=False, on_delete=models.CASCADE, verbose_name='reporte')

class Avances(models.Model):
    id_avance    = models.AutoField(primary_key=True)
    titulo       = models.CharField(max_length=255, null=False, verbose_name='titulo del reporte')
    descripcion  = models.TextField(null=False)
    fecha_avance = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')

    id_bug       = models.ForeignKey(Bug, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Bug')   
 
 
class Reasignacion(models.Model):
    ESTADOS_CHOICES    = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('desaprobado', 'Desaprobado')
    )
    
    id_avance          = models.AutoField(primary_key=True)
    fecha_reasignacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    
    id_programador     = models.ForeignKey(Programador, null=False, on_delete=models.CASCADE, verbose_name='Programador')
    id_bug             = models.ForeignKey(Bug, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Bug')   
    

class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    descripcion     = models.TextField(null=False)
    
    id_usuario      = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE, verbose_name='Usuario', related_name='reportes')
    id_programador  = models.ForeignKey(Programador, null=True, on_delete=models.CASCADE, verbose_name='Programador')
    id_bug          = models.ForeignKey(Bug, null=False, on_delete=models.CASCADE, verbose_name='Bug')  
    