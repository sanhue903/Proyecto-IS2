from django.db import models
from django.db.models import Q
import os
import uuid
##ver datetime para las fechas 


# Create your models here.

class Usuario(models.Model):
    class Meta:
        verbose_name        = 'usuario'
        verbose_name_plural = 'usuarios'
    
    
    id_usuario     = models.AutoField(primary_key=True)
    
    nombre_usuario = models.CharField(
        max_length=25, 
        blank=False,
        verbose_name='nombre',
    )
    
    correo_usuario = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='email',
    )

    #TODO ver encriptación de las contraseñas
    contraseña_usuario = models.CharField(
        max_length=25,
        blank=False,
    )
    
    
    def __str__(self):
        return self.nombre_usuario
    
    
    
class Programador(models.Model):    
    class Meta:
        verbose_name        = 'programador'
        verbose_name_plural = 'programadores'
        
        
    id_programador     = models.AutoField(primary_key=True)
    
    nombre_programador = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='nombre',
        )
    
    
    #TODO ver tema entre cuenta empleados para el login y este modelo
    correo_programador = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='email',
    )
    
    def __str__(self):
        return self.nombre_programador
    


class Proyecto(models.Model):
    class Meta:
        verbose_name        = 'proyecto'
        verbose_name_plural = 'proyectos'
        
        
    id_proyecto     = models.AutoField(primary_key=True)
    
    nombre_proyecto = models.CharField(
        max_length=255, 
        blank=False, 
        verbose_name='proyecto',
    )
    
    programadores   = models.ManyToManyField(
        Programador,
        through='Cargo',
    )


    def __str__(self):
        return self.nombre_proyecto
    
    

class Cargo(models.Model):
    id_programador = models.ForeignKey(
        Programador, 
        on_delete=models.CASCADE,   
        null=False,  
    )
    
    id_proyecto    = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        null=False,
    )
    
    cargo          = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='cargo del proyecto',
    )



class Bug(models.Model):
    class Meta:
        verbose_name        = 'caso de bug'
        verbose_name_plural = 'casos de bugs'
        
        
    PRIORIDADES_CHOICES = (
        ('BAJA'   , 'bug de baja prioridad'),
        ('MEDIA'  , 'bug de media prioridad'),
        ('ALTA'   , 'bug de alta prioridad'),
        ('URGENTE', 'bug de urgente prioridad'),
    )
    
    ESTADOS_CHOICES = (
        ('ASIGNADO'   , 'bug recien asignado'),
        ('EN PROCESO' , 'bug esta proceso de revisión'),
        ('SOLUCIONADO', 'bug solucionado'),
    )
    
    
    id_bug         = models.AutoField(primary_key=True)
    #TODO cambiar nombre de titulo
    titulo         = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Titulo del bug',
    )
    
    descripcion    = models.TextField(
        blank=False, 
        verbose_name='descripción',
    )
    
    prioridad      = models.CharField(
        max_length=50, 
        choices=PRIORIDADES_CHOICES, 
        verbose_name='prioridad',
    )
    
    estado         = models.CharField(
        max_length=50, 
        default=ESTADOS_CHOICES[0], 
        choices=ESTADOS_CHOICES, 
        verbose_name='estado',
    )
    
    fecha_reporte  = models.DateField(
        auto_now_add=True, 
        verbose_name='fecha del caso',
    )
    
    id_proyecto    = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE, 
        null=True, 
    )
    
    id_programador = models.ForeignKey(
        Programador,
        on_delete=models.CASCADE,
        null=False,
    )
    
    def __str__(self):
        return '{0.id_proyecto}_{0.id_bug}'.format(self)

    
class ReporteBug(models.Model):
    class Meta:
        verbose_name        = 'reporte de bug'
        verbose_name_plural = 'reportes de bugs'
    
    
    ESTADOS_CHOICES = (
        ('PENDIENTE'  , 'pendiente'),
        ('APROBADO'   , 'aprobado'),
        ('DESAPROBADO', 'desaprobado'),
    )
    
    
    id_reporte     = models.AutoField(primary_key=True)
    
    titulo         = models.CharField(
        max_length=255, 
        blank=False, 
        verbose_name='titulo del reporte',
    )
    
    reporte        = models.TextField(
        blank=False,
        verbose_name="descripción del reporte del bug",
    )
    
    fecha_reporte  = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='fecha de reporte'
    )
    
    estado         = models.CharField(
        max_length=50, 
        default=ESTADOS_CHOICES[0], 
        choices=ESTADOS_CHOICES, 
        verbose_name='estado del reporte'
    )
    
    correo_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE, 
        null=False, 
        verbose_name='usuario',
    )
    
    id_proyecto    = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='proyecto'
    )
    
    id_bug         = models.ForeignKey(
        Bug,
        on_delete=models.CASCADE,
        blank=True, 
        null=True,  
        verbose_name='caso del bug'
    )


    def __str__(self):
        return self.titulo


def custom_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return os.path.join('database/images', new_filename)

class Imagen(models.Model):
    class Meta:
        verbose_name        = 'imagen'
        verbose_name_plural = 'imagenes'
        
        
    id_imagen  = models.AutoField(primary_key=True)
    
    imagen     = models.ImageField(
        null=False,
        upload_to=custom_upload_to, 
        default="database/images/default.jpg"
    ) #definir ruta

    id_reporte = models.ForeignKey(
        ReporteBug,
        on_delete=models.CASCADE,
        null=False,  
        verbose_name='reporte de la imagen'
    )


class Avances(models.Model):
    class Meta:
        verbose_name        = 'avance'
        verbose_name_plural = 'avances'
        
        
    id_avance    = models.AutoField(primary_key=True)
    
    titulo       = models.CharField(
        max_length=255, 
        blank=False,
        verbose_name='titulo del reporte'
    )
    
    descripcion  = models.TextField(
        blank=False,
        verbose_name='descripción del reporte',
    )
    
    fecha_avance = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha de reporte'
    )

    id_bug       = models.ForeignKey(
        Bug,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='caso asociado'
    )  
    
    
    def __str__(self):
        return '{0.id_bug}_{0.id_avance}'.format(self)
 
 
class Reasignacion(models.Model):
    class Meta:
        verbose_name        = 'reasignación'
        verbose_name_plural = 'reasignaciones'
        
        
    ESTADOS_CHOICES        = (
        ('PENDIENTE'  , 'reasignación pendiente'),
        ('APROBADO'   , 'reasignación aprobada'),
        ('DESAPROBADO', 'reasignación desaprobada'),
    )
    
    
    id_reasignacion        = models.AutoField(primary_key=True)
    
    estado                 = models.CharField(
        max_length=50, 
        default=ESTADOS_CHOICES[0], 
        choices=ESTADOS_CHOICES, 
        verbose_name='estado de la reasignación'
    )
    
    fecha_reasignacion     = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha de la petición',
    )
    
    id_programador_inicial = models.ForeignKey(
        Programador,
        on_delete=models.CASCADE,
        null=False,  
        related_name='programadores_iniciales',
        related_query_name='programador_inicial',
        verbose_name='programador que pidio reasignación'
    )
    
    id_programador_final   = models.ForeignKey(
        Programador,
        on_delete=models.CASCADE,
        null=True,  
        related_name='programadores_reasignados',
        related_query_name='programador_reasignado',
        verbose_name='programador reasignado',
    )
       
    id_bug                 = models.ForeignKey(
        Bug, 
        on_delete=models.CASCADE,
        null=True, 
        verbose_name='caso del bug asociado',
    )   
    
    
    def __str__(self):
        return '{0.id_programador_inicial}_{0.id_bug}_{0.id_reasignacion}'.format(self)
    

class Notificaciones(models.Model):
    class Meta:
        verbose_name        = 'notificación'
        verbose_name_plural = 'notificaciones'
        
        
    id_notificacion = models.AutoField(primary_key=True)
    
    descripcion     = models.TextField(null=False)
    
    id_usuario      = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        null=True, 
        verbose_name='usuario'
    )
    
    id_programador  = models.ForeignKey(
        Programador,
        on_delete=models.CASCADE,
        null=True, 
        verbose_name='programador'
    
    )
    
    id_bug          = models.ForeignKey(
        Bug,
        on_delete=models.CASCADE,
        null=False, 
        verbose_name='caso del bug'
    )  
     
     
    def __str__(self):
        return '{0.id_bug}_{0.id_notificacion}'.format(self)
    