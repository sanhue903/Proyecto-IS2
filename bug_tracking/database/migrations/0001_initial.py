# Generated by Django 4.2 on 2023-05-31 20:26

import database.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id_bug', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255, verbose_name='Titulo del bug')),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('prioridad', models.CharField(choices=[('BAJA', 'Baja'), ('MEDIA', 'Media'), ('ALTA', 'Alta'), ('URGENTE', 'Urgente')], max_length=50, verbose_name='prioridad')),
                ('estado', models.CharField(choices=[('ASIGNADO', 'Asignado'), ('EN PROCESO', 'En revisión'), ('SOLUCIONADO', 'Solucionado')], default='ASIGNADO', max_length=50, verbose_name='estado')),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True, verbose_name='fecha del caso')),
            ],
            options={
                'verbose_name': 'caso de bug',
                'verbose_name_plural': 'casos de bugs',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=255, verbose_name='cargo del proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Programador',
            fields=[
                ('id_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'programador',
                'verbose_name_plural': 'programadores',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id_proyecto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proyecto', models.CharField(max_length=255, verbose_name='proyecto')),
                ('programadores', models.ManyToManyField(through='database.Cargo', to='database.programador')),
            ],
            options={
                'verbose_name': 'proyecto',
                'verbose_name_plural': 'proyectos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='ReporteBug',
            fields=[
                ('id_reporte', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255, verbose_name='titulo del reporte')),
                ('reporte', models.TextField(verbose_name='descripción del reporte del bug')),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True, verbose_name='fecha de reporte')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Arobado'), ('DESAPROBADO', 'Desaprobado')], default='PENDIENTE', max_length=50, verbose_name='estado del reporte')),
                ('id_bug', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.bug', verbose_name='caso del bug')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.proyecto', verbose_name='proyecto')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.usuario', verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
            },
        ),
        migrations.CreateModel(
            name='Reasignacion',
            fields=[
                ('id_reasignacion', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(verbose_name='razones de la reasignación')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobada'), ('DESAPROBADO', 'Desaprobada')], default='PENDIENTE', max_length=50, verbose_name='estado de la reasignación')),
                ('fecha_reasignacion', models.DateTimeField(auto_now_add=True, verbose_name='fecha de la petición')),
                ('id_bug', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.bug', verbose_name='caso del bug asociado')),
                ('id_programador_final', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programadores_reasignados', related_query_name='programador_reasignado', to='database.programador', verbose_name='programador reasignado')),
                ('id_programador_inicial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programadores_iniciales', related_query_name='programador_inicial', to='database.programador', verbose_name='programador que pidio reasignación')),
            ],
            options={
                'verbose_name': 'reasignación',
                'verbose_name_plural': 'reasignaciones',
            },
        ),
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notificación',
                'verbose_name_plural': 'notificaciones',
            },
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id_imagen', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(default='database/images/default.jpg', upload_to=database.models.custom_upload_to)),
                ('id_reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.reportebug', verbose_name='reporte de la imagen')),
            ],
            options={
                'verbose_name': 'imagen',
                'verbose_name_plural': 'imagenes',
            },
        ),
        migrations.AddField(
            model_name='cargo',
            name='id_programador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.programador'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='id_proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.proyecto'),
        ),
        migrations.AddField(
            model_name='bug',
            name='id_programador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.programador'),
        ),
        migrations.AddField(
            model_name='bug',
            name='id_proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.proyecto'),
        ),
        migrations.CreateModel(
            name='Avances',
            fields=[
                ('id_avance', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255, verbose_name='titulo del reporte')),
                ('descripcion', models.TextField(verbose_name='descripción del reporte')),
                ('fecha_avance', models.DateTimeField(auto_now_add=True, verbose_name='fecha de reporte')),
                ('id_bug', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.bug', verbose_name='caso asociado')),
            ],
            options={
                'verbose_name': 'reporte',
                'verbose_name_plural': 'reportes',
            },
        ),
    ]