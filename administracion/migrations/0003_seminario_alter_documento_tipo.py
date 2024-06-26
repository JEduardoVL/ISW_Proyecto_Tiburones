# Generated by Django 5.0.4 on 2024-05-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seminario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('ubicacion', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('presentador', models.CharField(max_length=100)),
                ('temas', models.TextField()),
                ('requisitos', models.TextField()),
                ('creditos_academicos', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
        ),
        migrations.AlterField(
            model_name='documento',
            name='tipo',
            field=models.CharField(choices=[('TT', 'Trabajo Terminal'), ('AR', 'Artículo'), ('TS', 'Tesis'), ('OT', 'Otro')], max_length=2),
        ),
    ]
