# Generated by Django 3.2 on 2022-11-08 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0018_auto_20221102_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='type',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
