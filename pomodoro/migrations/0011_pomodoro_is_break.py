# Generated by Django 3.2 on 2022-10-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomodoro', '0010_pomodoro_completed_cycle_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='pomodoro',
            name='is_break',
            field=models.BooleanField(default=False, help_text='Boolean Check for Break'),
        ),
    ]
