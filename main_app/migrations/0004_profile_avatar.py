# Generated by Django 3.1.5 on 2021-01-19 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210119_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]