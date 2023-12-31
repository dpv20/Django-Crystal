# Generated by Django 4.2.5 on 2023-10-13 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_delete_operacionfiltro_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDeLaLaguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien?')),
                ('cantidad', models.CharField(blank=True, max_length=200, null=True)),
                ('dotacion_incompleta', models.BooleanField(default=False)),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperacionLimpiezaManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien?')),
                ('equipamiento_incompleto', models.BooleanField(default=False, verbose_name='Incompleto')),
                ('equipamiento_defectuoso', models.BooleanField(default=False, verbose_name='Defectuoso')),
                ('Equipamiento_comentarios', models.TextField(blank=True, verbose_name='Equipamiento Comentarios')),
                ('bomba_en_mantencion', models.BooleanField(default=False, verbose_name='En mantención o reparación')),
                ('no_funciona_energia', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('no_funciona_electrico', models.BooleanField(default=False, verbose_name='No funciona por problema eléctrico o mecánico')),
                ('problemas_en_manguera', models.BooleanField(default=False, verbose_name='Problemas en la manguera')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('bomba_comentarios', models.TextField(blank=True, verbose_name='Bomba Limpieza Manual Comentarios')),
                ('no_optima', models.BooleanField(default=False, verbose_name='No óptima')),
                ('otro_secuencia', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('secuencia_comentarios', models.TextField(blank=True, verbose_name='Secuencia de Limpieza Comentarios')),
                ('suciedad_en_uniones', models.BooleanField(default=False, verbose_name='Suciedad en las uniones de liner, arrugas y baches')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentarios', models.TextField(blank=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperacionLimpiezaDeFondo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien?')),
                ('en_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('sin_combustible', models.BooleanField(default=False)),
                ('falla_mecanica', models.BooleanField(default=False)),
                ('problemas_en_piolas', models.BooleanField(default=False)),
                ('alarma_de_recalentamiento', models.BooleanField(default=False)),
                ('otro_motor_fuera_de_borda', models.CharField(blank=True, max_length=200)),
                ('motor_fuera_de_borda_comentario', models.TextField(blank=True)),
                ('filtracion_en_cuerpo', models.BooleanField(default=False)),
                ('filtracion_en_union_muro', models.BooleanField(default=False)),
                ('filtracion_en_union_carro', models.BooleanField(default=False)),
                ('filtracion_en_union_Y', models.BooleanField(default=False)),
                ('otro_tipo_de_filtracion', models.CharField(blank=True, max_length=200)),
                ('manguera_comentarios', models.TextField(blank=True)),
                ('bomba_en_mantencion', models.BooleanField(default=False)),
                ('no_funciona_energia', models.BooleanField(default=False)),
                ('no_funciona_electrico', models.BooleanField(default=False)),
                ('otro_bomba', models.CharField(blank=True, max_length=200)),
                ('bomba_comentarios', models.TextField(blank=True)),
                ('no_optima', models.BooleanField(default=False)),
                ('velocidad_excesiva', models.BooleanField(default=False)),
                ('otro_secuencia', models.CharField(blank=True, max_length=200)),
                ('secuencia_comentarios', models.TextField(blank=True)),
                ('cepillos_gastados_antiguo', models.BooleanField(default=False)),
                ('valvula_mal_estado_antiguo', models.BooleanField(default=False)),
                ('plancha_acero_rota', models.BooleanField(default=False)),
                ('ruedas_mal_estado', models.BooleanField(default=False)),
                ('faldon_externo_gastado', models.BooleanField(default=False)),
                ('faldon_interno_gastado', models.BooleanField(default=False)),
                ('otro_carro_antiguo', models.CharField(blank=True, max_length=200)),
                ('carro_antiguo_comentarios', models.TextField(blank=True)),
                ('cepillos_gastados_nuevo', models.BooleanField(default=False)),
                ('gomas_gastadas', models.BooleanField(default=False)),
                ('valvula_mal_estado_nuevo', models.BooleanField(default=False)),
                ('otro_carro_nuevo', models.CharField(blank=True, max_length=200)),
                ('carro_nuevo_comentarios', models.TextField(blank=True)),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentarios', models.TextField(blank=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperacionFiltro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('turbidez_media', models.BooleanField(default=False, verbose_name='Turbidez media')),
                ('sucia', models.BooleanField(default=False, verbose_name='Sucia')),
                ('otro_calidad_salida', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('calidad_salida_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('lecho_saturado', models.BooleanField(default=False, verbose_name='El lecho filtrante está saturado')),
                ('valvulas_no_funcionan', models.BooleanField(default=False, verbose_name='Las válvulas no abren y/o cierran bien')),
                ('filtracion_tuberias', models.BooleanField(default=False, verbose_name='Filtración de tuberías')),
                ('otro_filtro', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('filtro_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('turbidez_baja', models.BooleanField(default=False, verbose_name='Turbidez baja')),
                ('turbidez_media_camara', models.BooleanField(default=False, verbose_name='Turbidez media')),
                ('turbidez_alta', models.BooleanField(default=False, verbose_name='Turbidez alta')),
                ('otro_calidad_camara', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('calidad_camara_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('sensores_no_funcionan', models.BooleanField(default=False, verbose_name='Sensores no funcionan')),
                ('otro_sensores', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('sensores_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('bomba_en_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('no_funciona_energia_bomba', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('no_funciona_electrico_bomba', models.BooleanField(default=False, verbose_name='No funciona por problema eléctrico o mecánico')),
                ('problemas_variador', models.BooleanField(default=False, verbose_name='Problemas variador de frecuencia /Partidor Suave')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('bomba_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentarios', models.TextField(blank=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
