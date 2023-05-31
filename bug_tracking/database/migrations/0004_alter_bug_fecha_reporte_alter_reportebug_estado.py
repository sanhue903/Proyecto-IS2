# Generated by Django 4.2 on 2023-05-28 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_imagen_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='fecha_reporte',
            field=models.DateField(auto_now_add=True, verbose_name='fecha del caso'),
        ),
        migrations.AlterField(
            model_name='reportebug',
            name='estado',
            field=models.CharField(choices=[('PENDIENTE', 'en revisión'), ('APROBADO', 'aprobado'), ('DESAPROBADO', 'desaprobado')], default=('PENDIENTE', 'en revisión'), max_length=50, verbose_name='estado del reporte'),
        ),
    ]