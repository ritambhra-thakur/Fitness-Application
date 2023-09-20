# Generated by Django 3.2 on 2022-12-07 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_alter_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageEmoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=15, verbose_name='code')),
                ('name', models.CharField(max_length=15, verbose_name='Name')),
                ('file', models.ImageField(upload_to='emoji')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
