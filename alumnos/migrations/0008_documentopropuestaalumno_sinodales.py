# Generated by Django 5.0.3 on 2024-06-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0007_remove_documentopropuestaalumno_directores_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentopropuestaalumno',
            name='sinodales',
            field=models.BooleanField(default=False),
        ),
    ]