# Generated by Django 5.0 on 2024-02-16 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imop',
            old_name='last_recomendaciones_date',
            new_name='recomendaciones_date',
        ),
        migrations.RenameField(
            model_name='imop',
            old_name='last_resumen_ejecutivo_date',
            new_name='resumen_ejecutivo_date',
        ),
        migrations.RenameField(
            model_name='imop',
            old_name='last_temas_pendientes_date',
            new_name='temas_pendientes_date',
        ),
    ]
