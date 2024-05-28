# Generated by Django 5.0.3 on 2024-05-27 21:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento_alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_documento', models.CharField(max_length=255)),
                ('resumen', models.TextField()),
                ('nombre_autor', models.CharField(max_length=255)),
                ('sinodales', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('TT', 'Trabajo Terminal'), ('TE', 'Tesis'), ('OT', 'Otro')], max_length=2)),
                ('fecha_elaboracion', models.DateField()),
                ('convocatoria', models.CharField(max_length=255)),
                ('documento_url', models.URLField(blank=True, null=True)),
                ('archivo_subido', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]