# Generated by Django 3.2 on 2022-09-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_category_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.FileField(blank=True, help_text='Select file', null=True, upload_to='media/'),
        ),
    ]
