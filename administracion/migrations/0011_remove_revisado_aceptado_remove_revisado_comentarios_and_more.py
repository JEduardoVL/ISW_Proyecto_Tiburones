# Generated by Django 5.0.3 on 2024-06-03 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0010_revisarpropuesta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revisado',
            name='aceptado',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='comentarios',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='conclusiones_pertinentes',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='contenido_coherente',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='discusion_adecuada',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='documento_alumno',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='errores_ortograficos',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='estructura_clara',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='graficos_tablas_adecuados',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='introduccion_contextualiza',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='metodologia_descrita',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='normas_formato',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='objetivos_cumplidos',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='referencias_correctas',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='resultados_presentados',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='resumen_claro_conciso',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='revisado',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='suficientes_referencias',
        ),
        migrations.RemoveField(
            model_name='revisado',
            name='titulo_adecuado',
        ),
    ]
