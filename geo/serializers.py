import json

import psycopg2
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import GEOSGeometry, Point
from django.db import connections
from rest_framework import serializers

from geo.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ['ogc_fid', 'id', 'floor', 'status', 'data_in', 'function', 'id_style1', 'build_area',
                  'use_area', 'number_apa', 'population', 'seats', 'seats_cars', 'shape_leng', 'shape_le_1',
                  'shape_area', 'wkb_geometry']


class BusStopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BusStop
        fields = ['ogc_fid', 'stationnam', 'platformx', 'platformy', 'wkb_geometry']


class RedLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RedLine
        fields = ['ogc_fid', 'id_style', 'id_style1', 'shape_leng', 'shape_le_1', 'wkb_geometry']


class StreetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Street
        fields = ['ogc_fid', 'id', 'name', 'type', 'old_type', 'abreviatur', 'shape_leng', 'shape_le_1', 'wkb_geometry']


class DijkstraSerializer(serializers.Serializer):
    seq = serializers.IntegerField()
    path_seq = serializers.IntegerField()
    node = serializers.IntegerField()
    edge = serializers.IntegerField()
    cost = serializers.FloatField()
    agg_cost = serializers.FloatField()
    geom = serializers.SerializerMethodField()

    def get_geom(self, obj):
        try:
            geom = WaysVerticesPgr.objects.get(id=obj['node']).the_geom
        except Exception:
            return None
        return str(geom)


class VertexSerializer(serializers.Serializer):
    point_from_x = serializers.FloatField()
    point_from_y = serializers.FloatField()
    point_to_x = serializers.FloatField()
    point_to_y = serializers.FloatField()
    barrier = serializers.JSONField(required=False)
    closest_source = serializers.SerializerMethodField(required=False)
    closest_destination = serializers.SerializerMethodField(required=False)

    def get_closest_source(self, obj):
        point = Point(obj['point_from_x'], obj['point_from_y'], srid=4326)
        conn = connections['default']
        conn.ensure_connection()
        with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""SELECT streets.id AS node, streets.the_geom AS geometry, 
        ST_DISTANCE(streets.the_geom, '{point}'::geometry) AS distance
        FROM ways_vertices_pgr streets
        ORDER BY distance ASC
        LIMIT 1;""".format(point=point))
            row = cursor.fetchall()
        return row[0]

    def get_closest_destination(self, obj):
        point = Point(obj['point_to_x'], obj['point_to_y'], srid=4326)
        conn = connections['default']
        conn.ensure_connection()
        with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""SELECT streets.id AS node, streets.the_geom AS geometry, 
        ST_DISTANCE(streets.the_geom, '{point}'::geometry) AS distance
        FROM ways_vertices_pgr streets
        ORDER BY distance ASC
        LIMIT 1;""".format(point=point))
            row = cursor.fetchall()
        return row[0]


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'


class UploadGeometrySerializer(serializers.ModelSerializer):
    # color = serializers.CharField(required=False)
    class Meta:
        model = LayerFile
        fields = '__all__'
    #
    # def get_validation_exclusions(self):
    #     exclusions = super(UploadGeometrySerializer, self).get_validation_exclusions()
    #     return exclusions + ['color']


class HeatmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heatmap
        fields = '__all__'


class PointRadiusSerializer(serializers.Serializer):
    pointX = serializers.FloatField()
    pointY = serializers.FloatField()
    radius = serializers.IntegerField()
    file = serializers.FileField()


class VisibilityZonesSerializer(serializers.Serializer):
    observer_x = serializers.FloatField()
    observer_y = serializers.FloatField()
    observer_radius = serializers.IntegerField(default=150)
    observer_height = serializers.IntegerField(default=10)
    file = serializers.FileField()
    second_observer_x = serializers.FloatField(default=None)
    second_observer_y = serializers.FloatField(default=None)
    second_observer_radius = serializers.IntegerField(default=150)
    second_observer_height = serializers.IntegerField(default=10)
    second_file = serializers.FileField(default=None)


class CountObjectSerializer(serializers.Serializer):
    pointsNum = serializers.IntegerField()
    pointsList = serializers.ListField()
