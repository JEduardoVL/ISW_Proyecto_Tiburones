# Generated by Django 5.0.3 on 2024-06-02 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0006_directores_documentopropuestaalumno_directores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentopropuestaalumno',
            name='directores',
        ),
        migrations.DeleteModel(
            name='Directores',
        ),
    ]
