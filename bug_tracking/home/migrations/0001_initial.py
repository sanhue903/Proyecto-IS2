# Generated by Django 4.2 on 2023-05-18 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id_bug', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255, verbose_name='Titulo del bug')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('prioridad', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('urgente', 'Urgente')], max_length=20, verbose_name='Prioridad')),
                ('estado', models.CharField(choices=[('nuevo', 'Nuevo'), ('en proceso', 'En proceso'), ('solucionado', 'Solucionado')], max_length=20, verbose_name='Estado')),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteBug',
            fields=[
                ('id_reporte', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255, verbose_name='titulo del reporte')),
                ('reporte', models.TextField()),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')),
            ],
        ),
    ]
