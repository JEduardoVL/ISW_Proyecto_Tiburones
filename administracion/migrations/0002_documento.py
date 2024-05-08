# Generated by Django 5.0.3 on 2024-05-08 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('resumen', models.TextField()),
                ('palabras_clave', models.CharField(max_length=255)),
                ('nombre_autor', models.CharField(max_length=100)),
                ('sinodales', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('TT', 'Trabajo Terminal'), ('AR', 'Artículo'), ('OT', 'Otro')], max_length=2)),
                ('fecha_elaboracion', models.DateField()),
                ('convocatoria_titulacion', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
        ),
    ]
