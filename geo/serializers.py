from django.contrib.auth.models import User, Group
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


class VertexSerializer(serializers.Serializer):
    node_from = serializers.IntegerField()
    node_to = serializers.IntegerField()


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


class CountObjectSerializer(serializers.Serializer):
    pointX = serializers.FloatField()
    pointY = serializers.FloatField()
    radius = serializers.IntegerField()
    file = serializers.FileField()


class BufferOutputSerializer(serializers.Serializer):
    kppPoints = serializers.ListField()
    randomPoints = serializers.ListField()
