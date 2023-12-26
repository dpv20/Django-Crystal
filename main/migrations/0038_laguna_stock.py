# Generated by Django 4.2.5 on 2023-12-19 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_alter_laguna_identificador_alter_laguna_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laguna_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('stock_or_supply', models.CharField(choices=[('stock', 'Stock'), ('supply', 'Supply')], max_length=6)),
                ('cl_ap2hi', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cl_fh1lo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cl_flo12', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cl_cotflo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cl_mb010', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('laguna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.laguna', verbose_name='Project')),
            ],
        ),
    ]
