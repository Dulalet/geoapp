from django.contrib.auth.models import User, Group
from geo.models import Building, BusStop, RedLine, Street
from rest_framework import serializers


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
