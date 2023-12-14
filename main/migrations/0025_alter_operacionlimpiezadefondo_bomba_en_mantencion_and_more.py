# Generated by Django 4.2.5 on 2023-10-14 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_infraestructura_comentarios_muros_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacionlimpiezadefondo',
            name='bomba_en_mantencion',
            field=models.BooleanField(default=False, help_text='Bomba de Limpieza de Fondo'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezadefondo',
            name='cepillos_gastados_antiguo',
            field=models.BooleanField(default=False, help_text='Carro de aspiración(Antiguo)'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezadefondo',
            name='cepillos_gastados_nuevo',
            field=models.BooleanField(default=False, help_text='Carro de aspiración (Nuevo)'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezadefondo',
            name='en_mantencion',
            field=models.BooleanField(default=False, help_text='Motor fuera de borda (bote)', verbose_name='En mantención'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezadefondo',
            name='filtracion_en_cuerpo',
            field=models.BooleanField(default=False, help_text='Manguera de Limpieza de Fondo'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezadefondo',
            name='no_optima',
            field=models.BooleanField(default=False, help_text='Secuencia de Limpieza'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezamanual',
            name='bomba_en_mantencion',
            field=models.BooleanField(default=False, help_text='Bomba Limpieza Manual', verbose_name='En mantención o reparación'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezamanual',
            name='equipamiento_incompleto',
            field=models.BooleanField(default=False, help_text='Equipamiento', verbose_name='Incompleto'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezamanual',
            name='no_optima',
            field=models.BooleanField(default=False, help_text='Secuencia de Limpieza', verbose_name='No óptima'),
        ),
        migrations.AlterField(
            model_name='operacionlimpiezamanual',
            name='suciedad_en_uniones',
            field=models.BooleanField(default=False, help_text='Limpieza de Liner', verbose_name='Suciedad en las uniones de liner, arrugas y baches'),
        ),
    ]
