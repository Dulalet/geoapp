# Generated by Django 3.1.5 on 2021-04-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0021_auto_20210419_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='media',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='busstop',
            name='media',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='redline',
            name='media',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
