# Generated by Django 3.2 on 2022-11-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_timeline_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='number_of_days',
            field=models.IntegerField(verbose_name='Number of Days'),
        ),
    ]
