# Generated by Django 3.2 on 2022-11-10 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0019_auto_20221108_0606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
    ]
