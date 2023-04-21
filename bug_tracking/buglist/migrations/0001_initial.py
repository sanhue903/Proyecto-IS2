# Generated by Django 4.2 on 2023-04-21 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(verbose_name='Fecha de publición')),
                ('categoria', models.CharField(max_length=100)),
                ('prioridad', models.CharField(choices=[('H', 'Alta'), ('M', 'Media'), ('L', 'Baja')], default='M', max_length=1)),
            ],
        ),
    ]
