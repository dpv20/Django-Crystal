# Generated by Django 4.2.5 on 2023-12-26 18:24

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_rename_mymodel_imop'),
    ]

    operations = [
        migrations.AddField(
            model_name='imop',
            name='generated_id',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='imop',
            name='laguna',
            field=models.ForeignKey(default=main.models.get_default_laguna, on_delete=django.db.models.deletion.CASCADE, to='main.laguna'),
        ),
    ]
