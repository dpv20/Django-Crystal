# Generated by Django 4.2.5 on 2023-10-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_lagunaimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='LagoonDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idLagunas', models.CharField(max_length=50, verbose_name='Lagoon ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('comentrelevant', models.TextField(blank=True, null=True, verbose_name='Relevant Matters')),
                ('comentqw', models.TextField(blank=True, null=True, verbose_name='Comments on Water Quality')),
                ('comentlgm', models.TextField(blank=True, null=True, verbose_name='Comments on Lagoon Maintenance')),
                ('milestone', models.TextField(blank=True, null=True, verbose_name='Milestones')),
                ('responsible', models.CharField(blank=True, choices=[('Operations', 'Operations'), ('Engineering', 'Engineering')], max_length=20, null=True, verbose_name='Responsibility of the Milestone')),
                ('status', models.CharField(blank=True, choices=[('Normal Operation', 'Normal Operation'), ('Quarantine', 'Quarantine'), ('Emptying process', 'Emptying process'), ('Filling on going', 'Filling on going'), ('Quarantine/ Emptying process', 'Quarantine/ Emptying process')], max_length=50, null=True, verbose_name='Status')),
                ('showroom', models.BooleanField(default=False, verbose_name='Showroom Lagoon')),
            ],
        ),
    ]
