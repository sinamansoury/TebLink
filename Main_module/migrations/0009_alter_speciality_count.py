# Generated by Django 5.1.6 on 2025-03-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_module', '0008_alter_speciality_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciality',
            name='count',
            field=models.IntegerField(default=1, verbose_name='تعداد تخصص'),
        ),
    ]
