# Generated by Django 3.2 on 2022-09-28 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_type_type_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=15, verbose_name='Name'),
        ),
    ]
