# Generated by Django 4.2.5 on 2023-10-25 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_remove_laguna_idplatanus'),
    ]

    operations = [
        migrations.AddField(
            model_name='laguna',
            name='idplatanus',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
