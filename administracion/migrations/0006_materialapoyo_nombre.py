# Generated by Django 5.0.3 on 2024-05-23 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_alter_materialapoyo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialapoyo',
            name='nombre',
            field=models.CharField(default='sin nombre', max_length=255),
            preserve_default=False,
        ),
    ]