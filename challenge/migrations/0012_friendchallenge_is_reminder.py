# Generated by Django 3.2 on 2022-11-18 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0011_friendchallenge_parent_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendchallenge',
            name='is_reminder',
            field=models.BooleanField(default=True),
        ),
    ]
