# Generated by Django 5.1.5 on 2025-06-01 11:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_videos_uploaded_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 1, 16, 51, 43, 947021)),
        ),
    ]
