# Generated by Django 4.2.5 on 2023-10-13 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_operacionskimmers'),
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
