# Generated by Django 5.1.6 on 2025-02-18 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home_module', '0017_degree_remove_doctors_consultant_and_more'),
        ('Main_module', '0005_alter_consultant_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Consultant',
        ),
        migrations.DeleteModel(
            name='Speciality',
        ),
    ]
