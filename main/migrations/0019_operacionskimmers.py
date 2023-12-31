# Generated by Django 4.2.5 on 2023-10-13 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_funcionamientotelemetria'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperacionSkimmers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('bomba_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('bomba_no_energia', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('bomba_problemas_electricos', models.BooleanField(default=False, verbose_name='No funciona por problemas eléctricos o mecánicos')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('sensores_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('otro_sensores', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('sensores_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('agua_limpia', models.BooleanField(default=False, verbose_name='Limpia')),
                ('agua_turbidez_media', models.BooleanField(default=False, verbose_name='Turbidez media')),
                ('agua_sucia', models.BooleanField(default=False, verbose_name='Sucia')),
                ('otro_agua', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('agua_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('filtro_desgaste', models.BooleanField(default=False, verbose_name='Desgaste')),
                ('filtro_carcasa_no_cierra', models.BooleanField(default=False, verbose_name='Carcasa no cierra bien')),
                ('filtro_carcasa_rota', models.BooleanField(default=False, verbose_name='Carcasa rota')),
                ('otro_filtro', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('filtro_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('manguera_fisuras', models.BooleanField(default=False, verbose_name='Fisuras')),
                ('otro_manguera', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('manguera_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentario', models.TextField(blank=True, verbose_name='Comentarios')),
            ],
        ),
    ]
