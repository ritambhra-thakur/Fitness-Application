# Generated by Django 3.2 on 2022-10-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_otp_send_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_verification',
            field=models.BooleanField(default=True),
        ),
    ]
