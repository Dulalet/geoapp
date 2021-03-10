# Generated by Django 2.2.9 on 2021-03-10 18:52

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(blank=True, null=True)),
                ('floor', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('data_in', models.DateField(blank=True, null=True)),
                ('function', models.CharField(blank=True, max_length=100, null=True)),
                ('id_style1', models.IntegerField(blank=True, null=True)),
                ('build_area', models.FloatField(blank=True, null=True)),
                ('use_area', models.FloatField(blank=True, null=True)),
                ('number_apa', models.FloatField(blank=True, null=True)),
                ('population', models.FloatField(blank=True, null=True)),
                ('seats', models.FloatField(blank=True, null=True)),
                ('seats_cars', models.FloatField(blank=True, null=True)),
                ('shape_leng', models.FloatField(blank=True, null=True)),
                ('shape_le_1', models.FloatField(blank=True, null=True)),
                ('shape_area', models.FloatField(blank=True, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=3857)),
            ],
            options={
                'db_table': 'buildings_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('stationnam', models.CharField(blank=True, max_length=100, null=True)),
                ('platformx', models.CharField(blank=True, max_length=100, null=True)),
                ('platformy', models.CharField(blank=True, max_length=100, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=3857)),
            ],
            options={
                'db_table': 'bus_stops_project1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Heatmap',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fd1r05p1', models.TextField(blank=True, db_column='FD1R05P1', null=True)),
                ('fd1r06p1', models.TextField(blank=True, db_column='FD1R06P1', null=True)),
                ('fd1r06p2', models.TextField(blank=True, db_column='FD1R06P2', null=True)),
                ('fd1r072p1', models.TextField(blank=True, db_column='FD1R072P1', null=True)),
                ('fd1r07p1', models.TextField(blank=True, db_column='FD1R07P1', null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=32642)),
            ],
            options={
                'db_table': 'heatmap',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RedLine',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('id_style', models.CharField(blank=True, max_length=100, null=True)),
                ('id_style1', models.IntegerField(blank=True, null=True)),
                ('shape_leng', models.FloatField(blank=True, null=True)),
                ('shape_le_1', models.FloatField(blank=True, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=3857)),
            ],
            options={
                'db_table': 'red_lines_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('old_type', models.CharField(blank=True, max_length=100, null=True)),
                ('abreviatur', models.CharField(blank=True, max_length=100, null=True)),
                ('shape_leng', models.FloatField(blank=True, null=True)),
                ('shape_le_1', models.FloatField(blank=True, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=3857)),
            ],
            options={
                'db_table': 'streets_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Way',
            fields=[
                ('gid', models.BigAutoField(primary_key=True, serialize=False)),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('length_m', models.FloatField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('cost', models.FloatField(blank=True, null=True)),
                ('reverse_cost', models.FloatField(blank=True, null=True)),
                ('cost_s', models.FloatField(blank=True, null=True)),
                ('reverse_cost_s', models.FloatField(blank=True, null=True)),
                ('rule', models.TextField(blank=True, null=True)),
                ('one_way', models.IntegerField(blank=True, null=True)),
                ('oneway', models.TextField(blank=True, null=True)),
                ('x1', models.FloatField(blank=True, null=True)),
                ('y1', models.FloatField(blank=True, null=True)),
                ('x2', models.FloatField(blank=True, null=True)),
                ('y2', models.FloatField(blank=True, null=True)),
                ('maxspeed_forward', models.FloatField(blank=True, null=True)),
                ('maxspeed_backward', models.FloatField(blank=True, null=True)),
                ('priority', models.FloatField(blank=True, null=True)),
                ('the_geom', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'ways',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WaysVerticesPgr',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('osm_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('eout', models.IntegerField(blank=True, null=True)),
                ('lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('cnt', models.IntegerField(blank=True, null=True)),
                ('chk', models.IntegerField(blank=True, null=True)),
                ('ein', models.IntegerField(blank=True, null=True)),
                ('the_geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'ways_vertices_pgr',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20)),
                ('color', models.CharField(default='[255, 255, 255, 0.5]', max_length=25)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('geom', django.contrib.gis.db.models.fields.GeometryCollectionField(max_length=1000, srid=3857)),
            ],
        ),
        migrations.CreateModel(
            name='LayerFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('file', models.FileField(upload_to='layer_files')),
            ],
        ),
    ]
