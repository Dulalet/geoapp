# Generated by Django 3.1.5 on 2021-04-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0009_auto_20210415_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='ogc_fid',
            field=models.IntegerField(default=1075, unique=True),
            preserve_default=False,
        ),
    ]
