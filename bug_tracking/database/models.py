from django.db import models
from django.core.exceptions import ValidationError
import os
import uuid
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib import messages
# ver datetime para las fechas


# Create your models here.

class Usuario(models.Model):
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    id_user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_user.username


class Programador(models.Model):
    class Meta:
        verbose_name = 'programador'
        verbose_name_plural = 'programadores'

    id_user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_user.first_name + ' ' + self.id_user.last_name


@receiver(post_save, sender=User)
def crear_perfil_usuario_empleado(sender, instance, created, **kwargs):
    if created:
        if not instance.is_staff:
            Usuario.objects.create(id_user=instance)
            return

        if not instance.is_superuser:
            Programador.objects.create(id_user=instance)
            
            grupo = Group.objects.get(name='empleados')
            grupo.user_set.add(instance)
            


class Proyecto(models.Model):
    class Meta:
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'

    id_proyecto = models.AutoField(primary_key=True)

    nombre_proyecto = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='proyecto',
    )

    programadores = models.ManyToManyField(
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

    id_proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        null=False,
    )

    cargo = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='cargo del proyecto',
    )


class Bug(models.Model):
    class Meta:
        verbose_name = 'caso de bug'
        verbose_name_plural = 'casos de bugs'

    PRIORIDADES_CHOICES = (
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    )

    ESTADOS_CHOICES = (
        ('ASIGNADO', 'Asignado'),
        ('EN PROCESO', 'En revisión'),
        ('SOLUCIONADO', 'Solucionado'),
    )

    id_bug = models.AutoField(primary_key=True)
    # TODO cambiar nombre de titulo
    titulo = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Titulo del bug',
    )

    descripcion = models.TextField(
        blank=False,
        verbose_name='descripción',
    )

    prioridad = models.CharField(
        max_length=50,
        choices=PRIORIDADES_CHOICES,
        verbose_name='prioridad',
    )

    estado = models.CharField(
        max_length=50,
        default=ESTADOS_CHOICES[0][0],
        choices=ESTADOS_CHOICES,
        verbose_name='estado',
    )

    fecha_reporte = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha del caso',
    )

    id_proyecto = models.ForeignKey(
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
        return self.titulo


class ReporteBug(models.Model):
    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'

    ESTADOS_CHOICES = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Arobado'),
        ('DESAPROBADO', 'Desaprobado'),
    )

    id_reporte = models.AutoField(primary_key=True)

    titulo = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='titulo del reporte',
    )

    reporte = models.TextField(
        blank=False,
        verbose_name="descripción del reporte del bug",
    )

    fecha_reporte = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha de reporte'
    )
    
    estado         = models.CharField(
        max_length=50, 
        # 
        default=ESTADOS_CHOICES[0][0], 
        choices=ESTADOS_CHOICES, 

        verbose_name='estado del reporte'
    )

    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='usuario',
    )

    id_proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='proyecto'
    )

    id_bug = models.ForeignKey(
        Bug,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='caso del bug'
    )

    def __str__(self):
        return self.titulo

@receiver(pre_save, sender=ReporteBug)
def actualizar_id_bug(sender, instance, **kwargs):
    if instance.estado == ReporteBug.ESTADOS_CHOICES[0][0] and instance.id_bug:
        raise ValidationError("No se puede asignar caso del bug en estado pendiente")
    
    if instance.estado == ReporteBug.ESTADOS_CHOICES[1][0] and not instance.id_bug:
        raise ValidationError("No se puede guardar un reporte aprobado sin un caso de bug")
    
    if instance.estado == ReporteBug.ESTADOS_CHOICES[2][0] and instance.id_bug:
        raise ValidationError("No se puede guardar un caso de bug en un reporte desaprobado")

def custom_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return os.path.join('', new_filename)


class Imagen(models.Model):
    class Meta:
        verbose_name = 'imagen'
        verbose_name_plural = 'imagenes'

    id_imagen = models.AutoField(primary_key=True)

    imagen = models.ImageField(
        null=False,
        upload_to=custom_upload_to,
        default="database/images/default.jpg"
    )  # definir ruta

    id_reporte = models.ForeignKey(
        ReporteBug,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='reporte de la imagen'
    )


class Avances(models.Model):
    class Meta:
        verbose_name = 'reporte'
        verbose_name_plural = 'reportes'

    id_avance = models.AutoField(primary_key=True)

    titulo = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='titulo del reporte'
    )

    descripcion = models.TextField(
        blank=False,
        verbose_name='descripción del reporte',
    )

    fecha_avance = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha de reporte'
    )

    id_bug = models.ForeignKey(
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
        verbose_name = 'reasignación'
        verbose_name_plural = 'reasignaciones'

    ESTADOS_CHOICES = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobada'),
        ('DESAPROBADO', 'Desaprobada'),
    )

    id_reasignacion = models.AutoField(primary_key=True)
    
    comment = models.TextField(
        verbose_name='razones de la reasignación'
    )

    estado = models.CharField(
        max_length=50,
        default=ESTADOS_CHOICES[0][0],
        choices=ESTADOS_CHOICES,
        verbose_name='estado de la reasignación'
    )

    fecha_reasignacion = models.DateTimeField(
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

    id_programador_final = models.ForeignKey(
        Programador,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='programadores_reasignados',
        related_query_name='programador_reasignado',
        verbose_name='programador reasignado',
    )

    id_bug = models.ForeignKey(
        Bug,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='caso del bug asociado',
    )

    def __str__(self):
        return '{0.id_programador_inicial}_{0.id_bug}_{0.id_reasignacion}'.format(self)

    def clean(self):
        if self.id_programador_inicial == self.id_programador_final:
            raise ValidationError("No se puede reasignar a la misma persona.")


class Notificaciones(models.Model):
    class Meta:
        verbose_name        = 'notificación'
        verbose_name_plural = 'notificaciones'
  
    id_notificacion   = models.AutoField(primary_key=True)

    descripcion       = models.TextField(null=False)
    
    id_user           = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    
    fecha_notificacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha',
    )
    
    fue_leido          = models.BooleanField(default=False)

    def __str__(self):
        return '{0.id_notificacion}'.format(self)
