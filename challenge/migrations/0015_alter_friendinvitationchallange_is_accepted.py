# Generated by Django 3.2 on 2022-11-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0014_friendchallenge_is_reminder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendinvitationchallange',
            name='is_accepted',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
