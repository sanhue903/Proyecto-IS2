# Generated by Django 4.2 on 2023-06-22 21:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificaciones',
            name='fecha_notificacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='fecha'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notificaciones',
            name='fue_leido',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reasignacion',
            name='id_programador_final',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programadores_reasignados', related_query_name='programador_reasignado', to='database.programador', verbose_name='programador reasignado'),
        ),
    ]