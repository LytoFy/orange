# Generated by Django 2.2.4 on 2019-08-17 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_auto_20190817_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='handbook',
            name='name',
            field=models.CharField(default='手账模板', max_length=50, verbose_name='手账名'),
        ),
    ]