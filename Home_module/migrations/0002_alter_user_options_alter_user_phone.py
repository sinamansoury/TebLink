# Generated by Django 5.1.6 on 2025-02-13 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
