# Generated by Django 4.2.5 on 2023-10-25 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_laguna_idplatanus'),
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
