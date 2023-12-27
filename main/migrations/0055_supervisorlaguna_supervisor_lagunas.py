# Generated by Django 4.2.5 on 2023-12-27 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_laguna_filtroreporte'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorLaguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laguna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.laguna')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.supervisor')),
            ],
            options={
                'unique_together': {('supervisor', 'laguna')},
            },
        ),
        migrations.AddField(
            model_name='supervisor',
            name='lagunas',
            field=models.ManyToManyField(related_name='supervisors', through='main.SupervisorLaguna', to='main.laguna'),
        ),
    ]
