# Generated by Django 2.2 on 2022-04-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_post_mainphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mainphoto',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
