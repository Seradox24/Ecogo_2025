# Generated by Django 5.1.3 on 2024-12-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_usersacademy_anno_ingreso_usersacademy_cod_carrera_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersacademy',
            name='nom_carrera',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]