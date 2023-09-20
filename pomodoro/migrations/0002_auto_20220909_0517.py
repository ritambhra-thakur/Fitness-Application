# Generated by Django 3.2 on 2022-09-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomodoro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pomodoro',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='pomodoro',
            name='elapsed_time',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='pomodoro',
            name='name',
            field=models.CharField(blank=True, help_text='Enter the tittle name', max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pomodoro',
            name='total_time',
            field=models.DurationField(),
        ),
    ]
