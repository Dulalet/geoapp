# Generated by Django 3.1.5 on 2021-04-14 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0007_auto_20210414_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='is_general',
            field=models.BooleanField(default=False),
        ),
    ]
