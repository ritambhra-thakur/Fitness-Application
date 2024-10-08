# Generated by Django 3.2 on 2022-10-19 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_default_sound'),
        ('pomodoro', '0011_pomodoro_is_break'),
    ]

    operations = [
        migrations.AddField(
            model_name='pomodoro',
            name='chime_music_url',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='pomodoro',
            name='is_chime_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pomodoro',
            name='selected_music',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pomodoro_music', to='users.music'),
        ),
    ]
