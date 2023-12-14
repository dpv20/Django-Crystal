# Generated by Django 4.2.5 on 2023-10-13 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_remove_condicionliner_lagoon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperacionUltrasonido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('equipo_electronico_defectuoso', models.BooleanField(default=False, verbose_name='Equipo electrónico defectuoso')),
                ('agua_no_llega_transductores', models.BooleanField(default=False, verbose_name='El agua no llega a los transductores')),
                ('falta_energia', models.BooleanField(default=False, verbose_name='Falta de energía')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperacionSkimmers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
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
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperacionSistemaRecirculacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('bomba_en_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('no_funciona_energia', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('no_funciona_electrico', models.BooleanField(default=False, verbose_name='No funciona por problemas eléctricos o mecánicos')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('bomba_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('inyectores_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('caudal_bajo', models.BooleanField(default=False, verbose_name='Caudal bajo')),
                ('faltan_inyectores', models.BooleanField(default=False, verbose_name='Faltan inyectores por instalar')),
                ('otro_inyectores', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('inyectores_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('manifold_no_cierra', models.BooleanField(default=False, verbose_name='No cierra correctamente')),
                ('manifold_filtraciones', models.BooleanField(default=False, verbose_name='Con filtraciones')),
                ('otro_manifold', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('manifold_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('camara_filtraciones', models.BooleanField(default=False, verbose_name='Presenta filtraciones')),
                ('otro_camara', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('camara_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentario', models.TextField(blank=True, verbose_name='Comentario')),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperacionSistemaDosificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('nivel_bajo', models.BooleanField(default=False, verbose_name='Bajo')),
                ('nivel_critico', models.BooleanField(default=False, verbose_name='Crítico')),
                ('nivel_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('bomba_en_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('bomba_no_funciona_energia', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('bomba_no_funciona_electrico', models.BooleanField(default=False, verbose_name='No funciona por problemas eléctrico o mecánico')),
                ('bomba_no_marca_presion', models.BooleanField(default=False, verbose_name='No marca presión')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('bomba_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('filtracion_estanque', models.BooleanField(default=False, verbose_name='Filtración en estanque')),
                ('valvula_corte_dañadas', models.BooleanField(default=False, verbose_name='Vávula de corte dañadas')),
                ('otro_estanque', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('estanque_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('caudal_insuficiente', models.BooleanField(default=False, verbose_name='Insuficiente caudal bomba dosificadora')),
                ('valvulas_tapadas', models.BooleanField(default=False, verbose_name='Válvulas retención tapadas o defectuosas')),
                ('mangueras_incrustaciones', models.BooleanField(default=False, verbose_name='Mangueras o tuberías con incrustaciones')),
                ('venturi_mal_estado', models.BooleanField(default=False, verbose_name='Venturi en mal estado')),
                ('otro_venturi', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('venturi_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('bomba_playa_en_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('bomba_playa_no_funciona_energia', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('bomba_playa_no_funciona_electrico', models.BooleanField(default=False, verbose_name='No funciona por problemas eléctrico o mecánico')),
                ('otro_bomba_playa', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('bomba_playa_comentarios', models.TextField(blank=True, verbose_name='Comentarios')),
                ('discordancia_telemetria', models.BooleanField(default=False, verbose_name='Discordancia entre la dosificación por telemetría y la real')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentarios', models.TextField(blank=True)),
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
        migrations.CreateModel(
            name='NivelDeLaLaguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('nivel_bajo', models.BooleanField(default=False, verbose_name='Nivel bajo')),
                ('nivel_alto', models.BooleanField(default=False, verbose_name='Nivel alto')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedidasDeMitigacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('medidas_ineficientes', models.BooleanField(default=False, verbose_name='Medidas Ineficientes')),
                ('no_tienen', models.BooleanField(default=False, verbose_name='No tienen')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Infraestructura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('pintura_desgastada_playa', models.BooleanField(default=False, verbose_name='Pintura Desgastada')),
                ('focos_oxido_playa', models.BooleanField(default=False, verbose_name='Presencia de focos de óxido')),
                ('sucio_manchas_playa', models.BooleanField(default=False, verbose_name='Sucio/Manchas')),
                ('otro_playa', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('comentarios_playa', models.TextField(blank=True, verbose_name='Comentarios')),
                ('pintura_desgastada_muros', models.BooleanField(default=False, verbose_name='Pintura Desgastada')),
                ('sucio_manchas_muros', models.BooleanField(default=False, verbose_name='Sucio/Manchas')),
                ('otro_muros', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('comentarios_muros', models.TextField(blank=True, verbose_name='Comentarios')),
                ('sensores_mal_estado', models.BooleanField(default=False, verbose_name='Sensores de nivel en mal estado')),
                ('bomba_mal_estado', models.BooleanField(default=False, verbose_name='Bomba sentina en mal estado o no tienen')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FuncionamientoTelemetria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('conexion_problemas', models.BooleanField(default=False, verbose_name='Conexión con problemas')),
                ('otro_comunicacion', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('sin_conexion', models.BooleanField(default=False, verbose_name='Sin conexión')),
                ('velocidad_baja', models.BooleanField(default=False, verbose_name='Velocidad baja')),
                ('otro_internet', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('circuito_agua', models.BooleanField(default=False, verbose_name='Circuito eléctrico con agua')),
                ('sensor_temp_danado', models.BooleanField(default=False, verbose_name='Dañado')),
                ('sensor_temp_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('sensor_temp_fuera_rango', models.BooleanField(default=False, verbose_name='Fuera de rango')),
                ('otro_sensor_temp', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('sensor_orp_danado', models.BooleanField(default=False, verbose_name='Dañado')),
                ('sensor_orp_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('sensor_orp_fuera_rango', models.BooleanField(default=False, verbose_name='Fuera de rango')),
                ('otro_sensor_orp', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('turbidimetro_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('turbidimetro_danado', models.BooleanField(default=False, verbose_name='Dañado')),
                ('turbidimetro_fuera_rango', models.BooleanField(default=False, verbose_name='Fuera de rango')),
                ('otro_turbidimetro', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('bomba_potencia_insuficiente', models.BooleanField(default=False, verbose_name='No tiene la potencia necesaria')),
                ('bomba_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('pantalla_touch_no_funciona', models.BooleanField(default=False, verbose_name='Pantalla touch no funciona')),
                ('monitor_apagado', models.BooleanField(default=False, verbose_name='Apagado')),
                ('otro_monitor', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('panel_no_energizado', models.BooleanField(default=False, verbose_name='No energizado')),
                ('panel_no_funciona', models.BooleanField(default=False, verbose_name='No funciona')),
                ('otro_panel', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('evaluacion_comentario', models.TextField(blank=True, verbose_name='Comentario')),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FuncionamientoAguaRelleno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('bomba_mantencion', models.BooleanField(default=False, verbose_name='En mantención')),
                ('no_funciona_energia', models.BooleanField(default=False, verbose_name='No funciona por falta de energía')),
                ('no_funciona_electrico', models.BooleanField(default=False, verbose_name='No funciona por problema eléctrico o mecánico')),
                ('otro_bomba', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('sequia', models.BooleanField(default=False, verbose_name='Sequía')),
                ('cuentas_impagas', models.BooleanField(default=False, verbose_name='Cuentas de agua potable impagas')),
                ('calidad_no_cumple', models.BooleanField(default=False, verbose_name='Calidad de agua no cumple estándar de Crystal Lagoons')),
                ('otro_fuente', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CondicionVisualLaguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('opacidad_leve', models.BooleanField(default=False, verbose_name='Opacidad leve - turbidez media')),
                ('sucia_alta', models.BooleanField(default=False, verbose_name='Sucia - turbidez alta')),
                ('otro_turbidez', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('verdoso', models.BooleanField(default=False, verbose_name='Verdoso')),
                ('verde', models.BooleanField(default=False, verbose_name='Verde')),
                ('lechoso', models.BooleanField(default=False, verbose_name='Lechoso')),
                ('otro_color', models.CharField(blank=True, max_length=200, verbose_name='Otro')),
                ('liner_sedimento', models.BooleanField(default=False, verbose_name='Liner con sedimento')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CondicionLiner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supervisor', models.CharField(max_length=200)),
                ('todo_bien', models.BooleanField(default=False, verbose_name='¿Operando todo bien? Sí')),
                ('perforaciones_cortes', models.BooleanField(default=False, verbose_name='Liner con perforaciones y/o cortes')),
                ('carbonato', models.BooleanField(default=False, verbose_name='Liner con carbonato')),
                ('algas', models.BooleanField(default=False, verbose_name='Liner con algas')),
                ('nota', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('lagoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to='main.laguna')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
