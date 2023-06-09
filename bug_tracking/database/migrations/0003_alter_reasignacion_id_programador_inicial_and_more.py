# Generated by Django 4.2.1 on 2023-06-24 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_alter_reasignacion_id_programador_final'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reasignacion',
            name='id_programador_inicial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programadores_iniciales', related_query_name='programador_inicial', to='database.programador', verbose_name='programador que pidio reasignación'),
        ),
        migrations.AlterField(
            model_name='reportebug',
            name='id_bug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.bug', verbose_name='caso asociado'),
        ),
    ]
