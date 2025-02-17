# Generated by Django 5.1.6 on 2025-02-14 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_module', '0010_alter_doctors_speciality'),
        ('Main_module', '0002_alter_speciality_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='speciality_name',
            field=models.CharField(default=None, max_length=100, verbose_name='تخصص پزشک'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doctors',
            name='speciality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main_module.speciality', verbose_name='تخصص'),
        ),
    ]
