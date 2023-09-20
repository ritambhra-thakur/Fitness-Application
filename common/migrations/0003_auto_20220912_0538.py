# Generated by Django 3.2 on 2022-09-12 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='count',
            field=models.CharField(default=1, help_text='Enter the Code', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeline',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='timeline',
            name='is_active',
            field=models.BooleanField(default=False, help_text='active'),
        ),
        migrations.AddField(
            model_name='timeline',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='to delete the pomodoro'),
        ),
        migrations.AddField(
            model_name='timeline',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
