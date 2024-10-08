# Generated by Django 3.2 on 2022-09-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomodoro', '0003_pomodoro_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pomodoro',
            name='elapsed_time',
            field=models.DurationField(default=5),
        ),
        migrations.AlterField(
            model_name='pomodoro',
            name='total_time',
            field=models.DurationField(default=5),
        ),
    ]
