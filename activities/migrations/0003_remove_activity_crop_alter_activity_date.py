# Generated by Django 5.1.7 on 2025-03-24 13:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_alter_activity_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='crop',
        ),
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
