# Generated by Django 5.1.3 on 2024-12-12 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinador', '0002_alter_salidaterreno_actividad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salidaterreno',
            name='dias',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AlterField(
            model_name='salidaterreno',
            name='noches',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
    ]
