# Generated by Django 4.2.5 on 2023-12-26 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_alter_lagunaimage_photo_relevantmatters'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('resumen_ejecutivo', models.TextField()),
                ('last_resumen_ejecutivo_date', models.DateField(editable=False, null=True)),
                ('recomendaciones', models.TextField()),
                ('last_recomendaciones_date', models.DateField(editable=False, null=True)),
                ('temas_pendientes', models.TextField()),
                ('last_temas_pendientes_date', models.DateField(editable=False, null=True)),
            ],
        ),
    ]
