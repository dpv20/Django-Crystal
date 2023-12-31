# Generated by Django 4.2.5 on 2023-10-11 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_type_personaldelalaguna_action_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaldelalaguna',
            name='action',
        ),
        migrations.AlterField(
            model_name='personaldelalaguna',
            name='cantidad',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='personaldelalaguna',
            name='comentario',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personaldelalaguna',
            name='lagoon',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='personaldelalaguna',
            name='nota',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True),
        ),
        migrations.AlterField(
            model_name='personaldelalaguna',
            name='supervisor',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='personaldelalaguna',
            name='todo_bien',
            field=models.BooleanField(default=False, verbose_name='¿Operando todo bien?'),
        ),
    ]
