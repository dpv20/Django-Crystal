# Generated by Django 4.2.5 on 2023-10-25 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_laguna_idplatanus_temp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laguna',
            name='idplatanus_temp',
        ),
        migrations.AlterField(
            model_name='laguna',
            name='idplatanus',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
