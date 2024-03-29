# Generated by Django 3.1.5 on 2021-04-14 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geo', '0002_auto_20210414_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='layer',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='layer',
            name='slug',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='layer',
            name='type',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='layer',
            name='url',
            field=models.CharField(max_length=100),
        ),
    ]
