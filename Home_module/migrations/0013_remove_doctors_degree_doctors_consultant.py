# Generated by Django 5.1.6 on 2025-02-15 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_module', '0012_doctors_degree'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctors',
            name='degree',
        ),
        migrations.AddField(
            model_name='doctors',
            name='consultant',
            field=models.CharField(blank=True, choices=[('پزشک عمومی', 'پزشک عمومی'), ('متخصص', 'متخصص'), ('روانشناس', 'روانشناس')], max_length=100, null=True, verbose_name='دسته بندی'),
        ),
    ]
