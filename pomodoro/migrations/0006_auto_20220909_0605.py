# Generated by Django 3.2 on 2022-09-09 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomodoro', '0005_auto_20220909_0604'),
    ]

    operations = [
        migrations.AddField(
            model_name='pomodoro',
            name='elapsed_time',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pomodoro',
            name='total_time',
            field=models.BigIntegerField(default=300),
        ),
    ]
