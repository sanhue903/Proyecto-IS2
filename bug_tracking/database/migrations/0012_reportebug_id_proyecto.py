# Generated by Django 4.2 on 2023-04-28 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_alter_cargo_cargo_alter_cargo_id_programador_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportebug',
            name='id_proyecto',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='database.proyecto', verbose_name='Proyecto'),
            preserve_default=False,
        ),
    ]
